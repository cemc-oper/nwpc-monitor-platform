import {OrgRepoList, OrgMemberList} from './components'
import ReactDom, {render} from 'react-dom';

render(<OrgRepoList />, document.getElementById('org-repo-list-section'));
render(<OrgMemberList />, document.getElementById('org-member-list-section'));
