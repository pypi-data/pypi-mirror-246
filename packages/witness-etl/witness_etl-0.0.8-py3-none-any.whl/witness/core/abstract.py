#  Copyright (c) 2022.  Eugene Popov.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import logging
import os
from abc import ABCMeta, abstractmethod
from typing import Optional
import pendulum

log = logging.getLogger(__name__)


class AbstractBatch(metaclass=ABCMeta):

    data: list
    meta: Optional

    @abstractmethod
    def fill(self, extractor):
        raise NotImplemented

    @abstractmethod
    def push(self, loader):
        raise NotImplemented

    @abstractmethod
    def dump(self, uri: str):
        raise NotImplemented

    @abstractmethod
    def restore(self, uri: str):
        raise NotImplemented


class AbstractExtractor(metaclass=ABCMeta):

    def __init__(self, uri: Optional[str] = None, **kwargs):

        self.uri: Optional[str] = uri
        self.output = None
        self.extraction_timestamp: Optional[pendulum.DateTime] = None
        self.record_source: Optional[str] = None
        self.serializer: Optional[AbstractSerializer] = None
        self.is_unified = False
        self.short_rs = False

    def set_extraction_timestamp(self):
        setattr(self, 'extraction_timestamp', pendulum.now())

    def set_record_source(self, record_source: Optional[str] = None, shorten=False):
        if record_source is None:
            record_source = os.path.split(self.uri)[1] if shorten else self.uri
        setattr(self, 'record_source', record_source)

    def _set_unified_true(self):
        setattr(self, 'is_unified', True)

    @abstractmethod
    def extract(self):
        """
        An abstract method for data extraction.
        """
        self.set_extraction_timestamp()
        self.set_record_source()
        return self

    @abstractmethod
    def unify(self):
        """
        An abstract method for deserialization from data source.
        """
        raise NotImplementedError


class AbstractLoader(metaclass=ABCMeta):

    def __init__(self, uri: Optional[str] = None):

        self.uri: Optional[str] = uri
        self.batch = None
        self.meta_to_attach: Optional[dict] = None
        self.output = None
        self.serializer: Optional[AbstractSerializer] = None

    @abstractmethod
    def prepare(self, batch: AbstractBatch):
        """
        An abstract method of preparing data from a Batch object for loading.
        """
        self._set_batch(batch)

    @abstractmethod
    def attach_meta(self, meta_elements: Optional[list] = None):
        """
        An abstract method for attaching meta from Batch-object
        to data prepared for loading.
        """
        self._set_meta_to_attach(meta_elements)

    @abstractmethod
    def load(self):
        """
        An abstract method for loading data to destination store.
        """
        raise NotImplementedError

    def _set_batch(self, batch: AbstractBatch):
        setattr(self, 'batch', batch)

    def _set_meta_to_attach(self, meta_elements):
        try:
            meta = self.batch.meta
        except AttributeError:
            log.exception('No batch object was passed to loader.'
                          'Pass a batch object to "prepare" method first.')
            raise AttributeError('No batch object was passed to loader')
        if meta_elements is None:
            elements_to_attach = {element: str(getattr(meta, element)) for element in meta}
        else:
            elements_to_attach = {element: str(getattr(meta, element)) for element in meta_elements}

        setattr(self, 'meta_to_attach', elements_to_attach)


class AbstractSerializer(metaclass=ABCMeta):

    def to_batch(self, raw, *args, **kwargs) -> AbstractBatch:
        """
        An abstract method for serializing extracted data to unified batch format.
        """
        raise NotImplementedError

    def from_batch(self, data, *args, **kwargs):
        """
        An abstract method for deserializing data from unified batch format.
        """
        raise NotImplementedError
