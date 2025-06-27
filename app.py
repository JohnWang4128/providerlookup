from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Provider
from config import Config
import os
from sqlalchemy import or_

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/search')
    def search():
        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)
        state = request.args.get('state', '')
        city = request.args.get('city', '')
        
        providers_query = Provider.query
        
        if query:
            providers_query = providers_query.filter(
                or_(
                    Provider.npi.like(f'%{query}%'),
                    Provider.affiliation_legal_business_name.like(f'%{query}%'),
                    Provider.endpoint.like(f'%{query}%')
                )
            )
        
        if state:
            providers_query = providers_query.filter(Provider.affiliation_address_state == state)
            
        if city:
            providers_query = providers_query.filter(Provider.affiliation_address_city.like(f'%{city}%'))
        
        providers = providers_query.paginate(
            page=page, 
            per_page=app.config['PROVIDERS_PER_PAGE'],
            error_out=False
        )
        
        return render_template(
            'search.html', 
            providers=providers,
            query=query,
            state=state,
            city=city
        )
    
    @app.route('/provider/<npi>')
    def provider_details(npi):
        provider = Provider.query.filter_by(npi=npi).first_or_404()
        return render_template('provider_details.html', provider=provider)
    
    @app.route('/api/providers')
    def api_providers():
        query = request.args.get('query', '')
        state = request.args.get('state', '')
        city = request.args.get('city', '')
        limit = request.args.get('limit', 10, type=int)
        
        providers_query = Provider.query
        
        if query:
            providers_query = providers_query.filter(
                or_(
                    Provider.npi.like(f'%{query}%'),
                    Provider.affiliation_legal_business_name.like(f'%{query}%'),
                    Provider.endpoint.like(f'%{query}%')
                )
            )
        
        if state:
            providers_query = providers_query.filter(Provider.affiliation_address_state == state)
            
        if city:
            providers_query = providers_query.filter(Provider.affiliation_address_city.like(f'%{city}%'))
        
        providers = providers_query.limit(limit).all()
        
        results = []
        for provider in providers:
            results.append({
                'npi': provider.npi,
                'name': provider.affiliation_legal_business_name,
                'endpoint': provider.endpoint,
                'city': provider.affiliation_address_city,
                'state': provider.affiliation_address_state,
                'address': provider.full_address
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    @app.route('/api/states')
    def api_states():
        states = db.session.query(Provider.affiliation_address_state) \
            .filter(Provider.affiliation_address_state != None) \
            .distinct() \
            .order_by(Provider.affiliation_address_state) \
            .all()
        
        # Format results
        state_list = [state[0] for state in states if state[0]]
        
        return jsonify({
            'success': True,
            'states': state_list
        })
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app