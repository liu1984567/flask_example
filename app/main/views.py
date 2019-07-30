#view.py

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            newuser = User(username=form.name.data)
            db.session.add(newuser)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                print('New user %s, send a email to admin' % newuser.username)
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=newuser)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), known=session.get('known'))

#/user/liudonghao
@app.route('/user/<name>')
def user(name):
    print('hello /user/%s' % name)
    return render_template('user.html', name=name)
    #return '<h1>Hello, %s</h1>' % name

@app.route('/redirect/bing')
def jump_bing():
    return redirect('https://cn.bing.com/')

@app.route('/test/')
def test():
    #moment.include_moment()
    return '<h1>time: %s </h1>' % datetime.utcnow()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

