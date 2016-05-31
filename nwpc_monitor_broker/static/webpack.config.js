var path = require('path');

module.exports = {
    entry: {
        welcome: './app/welcome/welcome.js',
        org: ['./app/org/org.js', './app/org/components.js']
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: "[name].entry.js"
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                loaders: [ 'babel' ],
                exclude: /node_modules/,
                include: __dirname
            }
        ]
    }
};