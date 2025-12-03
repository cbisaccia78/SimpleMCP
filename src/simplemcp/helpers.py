class UTF8EncodingMixin:
    def encode_utf8(self) -> bytes:
        return self.model_dump_json().encode("utf-8") + b"\n"
