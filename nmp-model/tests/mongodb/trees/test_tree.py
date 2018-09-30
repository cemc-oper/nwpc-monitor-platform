# coding: utf-8
from datetime import datetime

import pytest

from nmp_model.mongodb.tree import TreeNode, TreeData, Tree


class TestTreeNode(object):
    def test_construction(self):
        tree_node = TreeNode()

        tree_node = TreeNode(
            type="status",
            name="sms_status_tree",
            blob_ticket_id=1
        )

        tree_node = TreeNode(
            type="aborted_tasks",
            name="sms_aborted_tasks_tree",
            blob_ticket_id=2
        )
        #
        # tree_node = TreeNode(
        #     type="not_existed_type",
        #     name="sms_aborted_tasks_tree",
        #     blob_ticket_id=3
        # )

    def test_to_dict(self):
        tree_node = TreeNode(
            type="status",
            name="sms_status_tree",
            blob_ticket_id=1
        )

        tree_node_dict = {
            '_cls': 'TreeNode',
            'type': 'status',
            'name': 'sms_status_tree',
            'blob_ticket_id': 1
        }

        assert tree_node.to_dict() == tree_node_dict


class TestTreeData(object):
    def test_construction(self):
        tree_data = TreeData()

        tree_data = TreeData(
            nodes=[
                TreeNode(
                    type="status",
                    name="sms_status_tree",
                    blob_ticket_id=1
                ),
                TreeNode(
                    type="aborted_tasks",
                    name="sms_aborted_tasks_tree",
                    blob_ticket_id=2
                )
            ]
        )

    def test_to_dict(self):
        tree_data = TreeData(
            nodes=[
                TreeNode(
                    type="status",
                    name="sms_status_tree",
                    blob_ticket_id=1
                ),
                TreeNode(
                    type="aborted_tasks",
                    name="sms_aborted_tasks_tree",
                    blob_ticket_id=2
                )
            ]
        )

        tree_data_dict = {
            'nodes': [
                {
                    '_cls': 'TreeNode',
                    'type': 'status',
                    'name': 'sms_status_tree',
                    'blob_ticket_id': 1
                },
                {
                    '_cls': 'TreeNode',
                    'type': 'aborted_tasks',
                    'name': 'sms_aborted_tasks_tree',
                    'blob_ticket_id': 2
                }
            ]
        }

        assert tree_data.to_dict() == tree_data_dict


class TestTree(object):
    def test_construction(self):
        tree = Tree()

        tree = Tree(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 9, 55, 0),
            data=TreeData(
                nodes=[
                    TreeNode(
                        type="status",
                        name="sms_status_tree",
                        blob_ticket_id=1
                    ),
                    TreeNode(
                        type="aborted_tasks",
                        name="sms_aborted_tasks_tree",
                        blob_ticket_id=2
                    )
                ]
            )
        )

    def test_set_data(self):
        tree = Tree(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 9, 55, 0)
        )

        tree_data = TreeData(
            nodes=[
                TreeNode(
                    type="status",
                    name="sms_status_tree",
                    blob_ticket_id=1
                ),
                TreeNode(
                    type="aborted_tasks",
                    name="sms_aborted_tasks_tree",
                    blob_ticket_id=2
                )
            ]
        )

        tree.set_data(tree_data)

        tree_data = {}
        with pytest.raises(TypeError):
            tree.set_data(tree_data)

    def test_to_dict(self):
        tree = Tree(
            ticket_id=1,
            owner='my',
            repo='my_repo',
            timestamp=datetime(2018, 9, 17, 9, 55, 0),
            data=TreeData(
                nodes=[
                    TreeNode(
                        type="status",
                        name="sms_status_tree",
                        blob_ticket_id=1
                    ),
                    TreeNode(
                        type="aborted_tasks",
                        name="sms_aborted_tasks_tree",
                        blob_ticket_id=2
                    )
                ]
            )
        )

        tree_dict = {
            'ticket_id': 1,
            'owner': 'my',
            'repo': 'my_repo',
            'timestamp': datetime(2018, 9, 17, 9, 55, 0),
            'data': {
                'nodes': [
                    {
                        '_cls': 'TreeNode',
                        'type': 'status',
                        'name': 'sms_status_tree',
                        'blob_ticket_id': 1
                    },
                    {
                        '_cls': 'TreeNode',
                        'type': 'aborted_tasks',
                        'name': 'sms_aborted_tasks_tree',
                        'blob_ticket_id': 2
                    }
                ]
            }
        }

        assert tree.to_dict() == tree_dict
