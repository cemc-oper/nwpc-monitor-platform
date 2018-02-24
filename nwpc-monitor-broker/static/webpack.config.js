const path = require('path');

module.exports = {
    devtool: "source-map",
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
        rules: [
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader?cacheDirectory=true'
                },
                exclude: /node_modules/,
                include: __dirname
            }
        ]
    }
};