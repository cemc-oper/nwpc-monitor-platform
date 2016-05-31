var OrgRepoList = React.createClass({
    getInitialState: function() {
        return {repo_list: []};
    },
    componentDidMount: function() {
        var component = this;
        component.setState({
            repo_list: [
            {name: 'nwpc_op'},
            {name: 'nwpc_qu'},
            {name: 'eps_nwpc_qu'}
        ]});
    },
    render: function() {
        var rows = [];
        this.state.repo_list.forEach(function (element, index, array) {
            rows.push(
                <p key={element.name}>{element.name}</p>
            )
        });
        return (
            <div>
                {rows}
            </div>
        );
    }
});

ReactDOM.render(<OrgRepoList />, document.getElementById('org-repo-list-section'));

var OrgMemberList = React.createClass({
    getInitialState:function() {
        return {
            member_list: []
        };
    },

    componentDidMount: function() {
        var component = this;
        component.setState({
            member_list:[
                {name: 'wangdp'},
                {name: 'cuiyj'},
                {name: 'wangyt'},
                {name: 'jiaxzh'}
            ]
        })
    },

    render: function() {
        var rows = [];
        this.state.member_list.forEach(function (element, index, array) {
            rows.push(
                <p key={element.name}>{element.name}</p>
            )
        });
        return (
            <div>
                {rows}
            </div>
        );
    }
});

ReactDOM.render(<OrgMemberList />, document.getElementById('org-member-list-section'));