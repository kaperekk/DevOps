import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)

    # Create empty temp file in temp dir
    tf = tempfile.NamedTemporaryFile()
    # Get video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # Write the content to tf
    tf.write(out.read())
    # use moviepy to create audio from video(tf)
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    # Save audio /temp/{video_id}.mp3
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # Add file to MongoDB
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)
    # add message to new que
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
