var fs = require('fs');
var minify = require('html-minifier').minify;
fs.readFile('./index.html', 'utf8', (err, data) => {
    if (err) {
        console.log(err)
        return
    }
    fs.writeFile('./index-min.html', minify(data, {
        removeComments: true,
        collapseWhitespace: true,
        minifyJS: true,
        minifyCSS: true
    }), function () {
        console.log('success');
    });
})