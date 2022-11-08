from core import app

if __name__ == '__main__':
    app.debug=True
    app.run(host='localhost', port=5000)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    
    
    
    