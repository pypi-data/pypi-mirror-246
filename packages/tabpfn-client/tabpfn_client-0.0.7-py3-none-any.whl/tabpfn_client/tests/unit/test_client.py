import unittest

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import numpy as np

from tabpfn_client.client import ServiceClient
from tabpfn_client.tests.mock_tabpfn_server import with_mock_server


class TestServiceClient(unittest.TestCase):
    def setUp(self):
        # setup data
        X, y = load_breast_cancer(return_X_y=True)
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y, test_size=0.33, random_state=42)

        self.client = ServiceClient()

    @with_mock_server()
    def test_try_connection(self, mock_server):
        mock_server.router.get(mock_server.endpoints.root.path).respond(200)
        self.assertTrue(self.client.try_connection())

    @with_mock_server()
    def test_try_connection_with_invalid_server(self, mock_server):
        mock_server.router.get(mock_server.endpoints.root.path).respond(404)
        self.assertFalse(self.client.try_connection())

    @with_mock_server()
    def test_register_user(self, mock_server):
        mock_server.router.post(mock_server.endpoints.register.path).respond(200, json={"message": "dummy_message"})
        self.assertTrue(self.client.register("dummy_email", "dummy_password", "dummy_password", "dummy_validation")[0])

    @with_mock_server()
    def test_register_user_with_invalid_email(self, mock_server):
        mock_server.router.post(mock_server.endpoints.register.path).respond(401, json={"detail": "dummy_message"})
        self.assertFalse(self.client.register("dummy_email", "dummy_password", "dummy_password", "dummy_validation")[0])

    @with_mock_server()
    def test_register_user_with_invalid_validation_link(self, mock_server):
        mock_server.router.post(mock_server.endpoints.register.path).respond(401, json={"detail": "dummy_message"})
        self.assertFalse(self.client.register("dummy_email", "dummy_password", "dummy_password", "dummy_validation")[0])

    @with_mock_server()
    def test_register_user_with_limit_reached(self, mock_server):
        mock_server.router.post(mock_server.endpoints.register.path).respond(401, json={"detail": "dummy_message"})
        self.assertFalse(self.client.register("dummy_email", "dummy_password", "dummy_password", "dummy_validation")[0])

    @with_mock_server()
    def test_invalid_auth_token(self, mock_server):
        mock_server.router.get(mock_server.endpoints.protected_root.path).respond(401)
        self.assertFalse(self.client.try_authenticate("fake_token"))

    @with_mock_server()
    def test_valid_auth_token(self, mock_server):
        mock_server.router.get(mock_server.endpoints.protected_root.path).respond(200)
        self.assertTrue(self.client.try_authenticate("true_token"))

    @with_mock_server()
    def test_predict_with_valid_train_set_and_test_set(self, mock_server):
        dummy_json = {"train_set_uid": 5}
        mock_server.router.post(mock_server.endpoints.upload_train_set.path).respond(
            200, json=dummy_json)

        self.client.upload_train_set(self.X_train, self.y_train)

        dummy_result = {"y_pred": [1, 2, 3]}
        mock_server.router.post(mock_server.endpoints.predict.path).respond(
            200, json=dummy_result)

        pred = self.client.predict(
            train_set_uid=dummy_json["train_set_uid"],
            x_test=self.X_test
        )
        self.assertTrue(np.array_equal(pred, dummy_result["y_pred"]))
