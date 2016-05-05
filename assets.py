from flask.ext.assets import Bundle

blog_js_bundle = Bundle(
    "assets/third-party/jquery/jquery.min.js",
    "assets/third-party/bootstrap/bootstrap.min.js",

    Bundle(
        "assets/blog/general.coffee",
        filters="coffeescript, rjsmin"
    ),

    output="compiled/blog.js"
)

blog_css_bundle = Bundle(
    "assets/third-party/bootstrap/bootstrap.min.css",

    Bundle(
        "assets/blog/general.scss",
        filters="pyscss, cssmin"
    ),

    output="compiled/blog.css"
)
