from website import create_app
#can import specific function bc website is a package

app = create_app()

if __name__ == '__main__': #makes sure this runs in main
    app.run(host = '0.0.0.0',port = 8080,debug=False) # turn off later good for debugging b4 prod
    #not a prod wsgi server

