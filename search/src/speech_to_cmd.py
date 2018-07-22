#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, random, sys
import pyaudio
import rospkg
import rospy
from std_msgs.msg import Empty, String

try:
    # Python 2.x
    from sphinxbase import Config
    from pocketsphinx import Decoder
except ImportError:
    # Python 3.x
    from pocketsphinx.pocketsphinx import *
    from sphinxbase.sphinxbase import *

def search_feedback(msg):
    os.system('echo "{}" | festival --tts --language russian'.format(msg.data))

if __name__ == '__main__':
    rospy.init_node('speech_to_cmd')
    search_start_pub = rospy.Publisher('/search_start', Empty, queue_size=1)
    search_cancel_pub = rospy.Publisher('/search_cancel', Empty, queue_size=1)
    shot_pub = rospy.Publisher('/shot', Empty, queue_size=1)
    rospy.Subscriber("/search_feedback", String, search_feedback)

    rospack = rospkg.RosPack()
    pkg_path=rospack.get_path('search')

    phrase_start_set = [
        'слушаюсь хозяин',
        'сэр йес сэр',
        'вас понял конец связи',
        'с радостью',
    ]

    phrase_cancel_set = [
        'угу',
        'сделаю',
        'попробуем',
        'ок',
        'если настааиваешь',
        'так точно'
    ]

    phrase_shot_set = [
        'дело сделано',
        'мишн комплитэд',
        'задание выполнено, конец связи'
    ]

    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(pkg_path, 'psx/zero_ru.cd_cont_4000'))
    config.set_string('-jsgf', os.path.join(pkg_path, 'psx/gram.jsgf'))
    config.set_string('-dict', os.path.join(pkg_path, 'psx/ru.dic'))
    # config.set_string('-logfn', '/dev/null')

    phrase = ''

    decoder = Decoder(config)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    in_speech_bf = True

    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)

            if decoder.get_in_speech():
                sys.stdout.write('.')
                sys.stdout.flush()

            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()

                if not in_speech_bf:
                    decoder.end_utt()

                    try:
                        print(decoder.hyp().hypstr)
                        phrase = decoder.hyp().hypstr
                        if phrase == "пайкон наведение":
                            os.system('echo "{}" | festival --tts --language russian'.format(random.choice(phrase_start_set)))
                            search_start_pub.publish()
                        elif phrase == "пайкон отмена":
                            os.system('echo "{}" | festival --tts --language russian'.format(random.choice(phrase_cancel_set)))
                            search_cancel_pub.publish()
                        elif phrase == "пайкон огонь":
                            os.system('echo "{}" | festival --tts --language russian'.format(random.choice(phrase_shot_set)))
                            shot_pub.publish()

                    except AttributeError:
                        pass

                    decoder.start_utt()
        else:
            break
    decoder.end_utt()
