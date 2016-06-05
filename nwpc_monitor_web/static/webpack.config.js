var path = require('path');

module.exports = {
    devtool: "cheap-module-eval-source-map",
    entry: {
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
            },
            {
                test: /\.css$/,
                loader: "style!css"
            }
        ]
    },
    externals: {
    }
};