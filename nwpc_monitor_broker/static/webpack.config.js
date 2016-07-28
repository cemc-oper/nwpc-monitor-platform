var path = require('path');

module.exports = {
    devtool: "cheap-module-eval-source-map",
    entry: {
        welcome: './app/welcome/welcome.js',
        org: [
            './app/org/index.js'
        ],
        repo: [
            './app/repo/index.js'
        ],
        user: './app/user/index.js'
    },
    output: {
        path: path.join(__dirname, 'dist'),
        filename: "[name].entry.js",
        sourceMapFilename: '[file].map'
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
    },
    externals: {
        'react': 'React',
        'react-dom': 'ReactDOM',
        'redux': 'Redux',
        'react-redux': 'ReactRedux'
    }
};