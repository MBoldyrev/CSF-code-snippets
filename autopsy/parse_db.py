#!/usr/bin/python3

image_name = "reporting.E01" # the name given in acquisition task
volume_name = "vol_vol3" # assigned by Autopsy

import sqlite3, json, datetime

def datetime_from_timestamp( unix_timestamp ):
        return datetime.datetime.fromtimestamp(
                int( unix_timestamp )
            ).strftime('%Y-%m-%d %H:%M:%S GMT')

all_data = {
    "Views": {
        "Deleted Files": []
    },
    "Results": {
        "Extension Mismatch Detected": []
    }
}

sqlite3.connect('autopsy.db')
c = conn.cursor()

# Extension Mismatch
ext_mism_list = all_data["Results"]["Extension Mismatch Detected"]
for row in c.execute( '''
        select name, parent_path, mime_type, size, mtime, atime, crtime, ctime, md5, tsk_files.obj_id, artifact_id
        from tsk_files inner join blackboard_artifacts on blackboard_artifacts.obj_id = tsk_files.obj_id 
        where blackboard_artifacts.artifact_type_id = 34
        ''' ):
    ext_mism_list.append( {
        "visible_values": {
            "Source File":      row[0],
            "Extension":        row[0].split('.')[-1],
            "MIME Type":        row[2],
            "Data Source":      image_name
        },
        "File Metadata": {
            "Name":             row[0],
            "Type":             "File System",
            "MIME Type":        row[2],
            "Size":             row[3],
            "File Name Allocation": "Allocated",
            "Metadata Allocation": "Allocated",
            "Modified":         datetime_from_timestamp( row[4] ),
            "Accessed":         datetime_from_timestamp( row[5] ),
            "Created":          datetime_from_timestamp( row[6] ),
            "Changed":          datetime_from_timestamp( row[7] ),
            "MD5":              row[8],
            "Hash Lookup Results": "UNKNOWN",
            "Internal ID":      row[9]
        },
        "Results": {
            "Source File Path": "/{0}/{1}/{2}{3}".format(
                image_name, volume_name, row[1], row[0] ),
            "Artifact ID":      row[10]
        }
    } )
