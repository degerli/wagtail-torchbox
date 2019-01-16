from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class StreamFieldSerialiser:
    def serialise_struct_block(self, block, value):
        blocks = {}
        for field_name, value in value.items():
            child_block = block.child_blocks[field_name]
            blocks[field_name] = self.serialise_block(child_block, value)

        return blocks

    def serialise_list_block(self, block, value):
        blocks = []
        for child_value in value:
            blocks.append(self.serialise_block(block.child_block, child_value))

        return blocks

    def serialise_stream_block(self, value):
        blocks = []
        for child_block in value:
            blocks.append({
                'type': child_block.block_type,
                'value': self.serialise_block(child_block.block, child_block.value),
            })

        return blocks

    def serialise_block(self, block, value):
        if hasattr(block, 'to_graphql_representation'):
            return block.to_graphql_representation(value)
        elif isinstance(block, blocks.RichTextBlock):
            return value.source
        elif isinstance(block, EmbedBlock):
            # FIXME
            return {
                'url': value.url,
            }
        elif isinstance(block, ImageChooserBlock):
            # FIXME
            return {
                'id': value.id,
                'alt': value.title,
            }
        elif isinstance(block, blocks.FieldBlock):
            return value
        elif isinstance(block, blocks.StructBlock):
            return self.serialise_struct_block(block, value)
        elif isinstance(block, blocks.ListBlock):
            return self.serialise_list_block(block, value)
        elif isinstance(block, blocks.StreamBlock):
            return self.serialise_stream_block(block, value)
