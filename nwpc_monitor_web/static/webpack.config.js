var path = require('path');

module.exports = {
    devtool: "source-map",
    entry: {
        welcome: './app/welcome/index.js',
        'operation-system': './app/operation-system/index.js',
        'hpc': './app/hpc/index.js'
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
        'react-redux': 'ReactRedux',
        'echarts': 'echarts'
    }
};