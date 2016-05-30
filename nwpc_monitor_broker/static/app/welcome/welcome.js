var ExploreOwnerApp = React.createClass({
    getInitialState: function() {
        return {owner: ''};
    },
    onChange: function(e) {
        this.setState({owner: e.target.value});
    },
    handleSubmit: function(e) {
        e.preventDefault();
        console.log(this.state.owner);
        window.location.href='/'+this.state.owner;
    },
    render: function() {
        return (
            <div>
                <form className="form-inline" onSubmit={this.handleSubmit}>
                    <div className="form-group">
                        <input type="text" className="form-control" placeholder="用户名" onChange={this.onChange} value={this.state.owner} />
                        <button type="submit" className="btn btn-default">确定</button>
                    </div>
                </form>
            </div>
        );
    }
});

ReactDOM.render(<ExploreOwnerApp />, document.getElementById('explore-owner-section'));