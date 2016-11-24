var path = require('path');
var webpack = require('webpack');


var entry= {
    welcome: './app/welcome/index.js',
    'operation-system': './app/operation-system/index.js',
    'hpc': './app/hpc/index.js'
};

var webpack_module= {
    loaders: [
        {
            test: /\.js$/,
            loaders: [ 'babel' ],
            exclude: /node_modules/,
            include: __dirname
        }
    ]
};

var externals= {
    'react': 'React',
    'react-dom': 'ReactDOM',
    'redux': 'Redux',
    'react-redux': 'ReactRedux',
    'echarts': 'echarts',
    'moment': 'moment',
    'react-router': 'ReactRouter',
    'react-router-redux': 'ReactRouterRedux',
    'redux-thunk': 'ReduxThunk'
};

if( process.env.NODE_ENV == 'production' ) {
    module.exports = {
        entry: entry,
        output: {
            path: path.join(__dirname, 'dist'),
            filename: "[name].entry.min.js",
            sourceMapFilename: '[file].map'
        },
        module: webpack_module,
        externals: externals,
        plugins: [
            new webpack.optimize.UglifyJsPlugin({
                test: /(\.jsx|\.js)$/,
                compress: {
                    warnings: false
                },
            })
        ]
    };
}else{
    console.log('use develop build');
    module.exports = {
        devtool: "source-map",
        entry: entry,
        output: {
            path: path.join(__dirname, 'dist'),
            filename: "[name].entry.js",
            sourceMapFilename: '[file].map'
        },
        module: webpack_module,
        externals: externals
    };
}
