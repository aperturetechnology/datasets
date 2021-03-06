# coding=utf-8
# Copyright 2019 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Base TestCase to use test_data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import os
import tempfile

from absl.testing import absltest
import six
import tensorflow as tf
from tensorflow_datasets.core import dataset_info



GCS_ACCESS_FNS = {
    "original": dataset_info.gcs_dataset_files,
    "dummy": lambda _: []
}


class TestCase(tf.test.TestCase):
  """Base TestCase to be used for all tests.

  `test_data` class attribute: path to the directory with test data.
  `tmp_dir` attribute: path to temp directory reset before every test.
  """

  @classmethod
  def setUpClass(cls):
    super(TestCase, cls).setUpClass()
    cls.test_data = os.path.join(os.path.dirname(__file__), "test_data")
    # Test must not communicate with GCS.
    dataset_info.gcs_dataset_files = GCS_ACCESS_FNS["dummy"]

  @contextlib.contextmanager
  def gcs_access(self):
    # Restore GCS access
    dataset_info.gcs_dataset_files = GCS_ACCESS_FNS["original"]
    yield
    # Revert access
    dataset_info.gcs_dataset_files = GCS_ACCESS_FNS["dummy"]

  def setUp(self):
    super(TestCase, self).setUp()
    # get_temp_dir is actually the same for all tests, so create a temp sub-dir.
    self.tmp_dir = tempfile.mkdtemp(dir=tf.compat.v1.test.get_temp_dir())

  def assertRaisesWithPredicateMatch(self, err_type, predicate):
    if isinstance(predicate, six.string_types):
      predicate_fct = lambda err: predicate in str(err)
    else:
      predicate_fct = predicate
    return super(TestCase, self).assertRaisesWithPredicateMatch(
        err_type, predicate_fct)

