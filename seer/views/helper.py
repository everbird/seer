# -*- coding: utf-8 -*-

def program_entry(program):
    return dict(
            id=program.id,
            pid=program.pid,
            name=program.name,
            channel_id=program.channel_id,
            channel=channel_entry(program.channel),
            length=program.length,
            datenum=program.datenum,
            start_dt=datetime_entry(program.start_dt),
            end_dt=datetime_entry(program.end_dt),
            update_dt=datetime_entry(program.update_dt),
            )

def channel_entry(channel):
    return dict(
            priority=channel.priority,
            id=channel.id,
            name=channel.name
            )

def datetime_entry(dt):
    return dt.isoformat()
