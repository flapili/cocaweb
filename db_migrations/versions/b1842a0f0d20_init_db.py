"""init db

Revision ID: b1842a0f0d20
Revises: 
Create Date: 2021-05-08 16:51:47.073504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1842a0f0d20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('discord_stats_user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('discriminator', sa.Text(), nullable=False),
    sa.Column('avatar', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discord_stats_guild',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('icon', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['discord_stats_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discord_stats_channel',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('guild_id', sa.BigInteger(), nullable=False),
    sa.Column('nsfw', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['guild_id'], ['discord_stats_guild.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discord_stats_member',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('guild_id', sa.BigInteger(), nullable=False),
    sa.Column('display_name', sa.Text(), nullable=True),
    sa.Column('joined_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['guild_id'], ['discord_stats_guild.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['discord_stats_user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'guild_id')
    )
    op.create_index(op.f('ix_discord_stats_member_guild_id'), 'discord_stats_member', ['guild_id'], unique=False)
    op.create_index(op.f('ix_discord_stats_member_user_id'), 'discord_stats_member', ['user_id'], unique=False)
    op.create_table('discord_stats_message',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('author_id', sa.BigInteger(), nullable=False),
    sa.Column('guild_id', sa.BigInteger(), nullable=False),
    sa.Column('channel_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['discord_stats_user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['channel_id'], ['discord_stats_channel.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['guild_id'], ['discord_stats_guild.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discord_stats_message_author_id'), 'discord_stats_message', ['author_id'], unique=False)
    op.create_index(op.f('ix_discord_stats_message_channel_id'), 'discord_stats_message', ['channel_id'], unique=False)
    op.create_index(op.f('ix_discord_stats_message_guild_id'), 'discord_stats_message', ['guild_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_discord_stats_message_guild_id'), table_name='discord_stats_message')
    op.drop_index(op.f('ix_discord_stats_message_channel_id'), table_name='discord_stats_message')
    op.drop_index(op.f('ix_discord_stats_message_author_id'), table_name='discord_stats_message')
    op.drop_table('discord_stats_message')
    op.drop_index(op.f('ix_discord_stats_member_user_id'), table_name='discord_stats_member')
    op.drop_index(op.f('ix_discord_stats_member_guild_id'), table_name='discord_stats_member')
    op.drop_table('discord_stats_member')
    op.drop_table('discord_stats_channel')
    op.drop_table('discord_stats_guild')
    op.drop_table('discord_stats_user')
    # ### end Alembic commands ###
