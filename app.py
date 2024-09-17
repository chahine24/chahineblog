import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# مسار المجلد لحفظ الصور والفيديوهات
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.secret_key = 'your_secret_key'
# قائمة المدونات
posts = []


@app.route('/')
def blog_list():
    return render_template('blog_list.html', posts=posts)

# نموذج تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # تحقق من بيانات الاعتماد
            session['logged_in'] = True
            return redirect(url_for('blog_list'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

# مسار لتسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('blog_list'))


@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        video = request.files['video']
        video_url = request.form['video_url']  # رابط الفيديو الخارجي
        external_link = request.form['external_link']

        # حفظ الصورة إذا كانت موجودة
        image_filename = None
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # حفظ الفيديو إذا كان مرفوعاً من الجهاز
        video_filename = None
        if video:
            video_filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

        # إضافة المدونة إلى القائمة
        posts.append({
            'title': title,
            'content': content,
            'image': image_filename,
            'video': video_filename if video else None,  # إذا كان هناك فيديو مرفوع
            'video_url': video_url if not video else None,  # إذا كان هناك رابط فيديو
            'external_link': external_link
        })
        return redirect(url_for('blog_list'))

    return render_template('add_blog.html')


@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = posts[post_id - 1]
    return render_template('view_post.html', post=post)


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_blog(post_id):
    post = posts[post_id - 1]

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        video = request.files['video']
        video_url = request.form['video_url']
        external_link = request.form['external_link']

        # تحديث الصورة إذا كانت موجودة
        if image:
            image_filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            post['image'] = image_filename

        # تحديث الفيديو إذا كان مرفوعاً من الجهاز
        if video:
            video_filename = video.filename
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
            post['video'] = video_filename

        # تحديث المعلومات الأخرى
        post.update({
            'title': title,
            'content': content,
            'video_url': video_url if not video else post.get('video_url'),
            'external_link': external_link
        })

        return redirect(url_for('view_post', post_id=post_id))

    return render_template('edit_blog.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
