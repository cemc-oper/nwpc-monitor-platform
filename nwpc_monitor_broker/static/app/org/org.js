var OrgRepoList = React.createClass({
    getInitialState: function() {
        return {repo_list: [
            {name:1},
            {name:2},
            {name:3}
        ]};
    },
    componentDidMount: function() {
        var component = this;
    },
    render: function() {
        var rows = [];
        return (
            <div>
                    {
                        this.state.repo_list.map(function(an_repo) {
                            return <p>{an_repo.name}</p>;
                        })
                    }
            </div>
        );
    }
});

ReactDOM.render(<OrgRepoList />, document.getElementById('org-repo-list-section'));