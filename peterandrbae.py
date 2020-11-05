from Faces import Detection
from Utils import help
import streamlit as st
from PIL import Image
import numpy as np
import base64


def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    st.image('Gifs/combined.gif', use_column_width=True)
    st.image('Gifs/pete.gif', use_column_width=True)
    st.image('Gifs/combined.gif', use_column_width=True)


    help.newLine(lines=5)

    wikipedia_link = 'https://en.wikipedia.org/wiki/Peter_Andre'
    st.markdown('<h2 style="text-align:center;"> <span style="color:#F633FF">Peter '
                'André</span> is the greatest singer known to man</h2> '
                '<h2 style="text-align:center;"><span style="color:#19E12A">✌️👇 Fact   👇  👆</span><br><br>  <a '
                'href=https://en.wikipedia.org/wiki/Peter_Andre>Petey</a> '
                'is original <span style="color:#FFCD33">bae</span> ✨<br><br><span style="color:#19E12A">👇  👆 '
                'Fact   ✌️👇 </span><br><br> Mysterious girl is the best song ever <br><br><span '
                'style="color:#19E12A">✌️👇 Fact   👇  👆 </span></h2>',
                unsafe_allow_html=True)

    help.newLine(lines=3)

    st.video('https://www.youtube.com/watch?v=iqIq4B1rgl4')

    help.newLine(lines=3)

    st.markdown('<h2 style="text-align:center; background-color:#F633FF;"><span style="color:white">'
                ' ❤️🧡💛💚💙💜🖤<br>PETE-OOh<br>'
                ' ❤️🧡💛💚💙💜🖤<br>PETE-OOh<br>'
                ' ❤️🧡💛💚💙💜🖤<br>PETE-OOh<br>'
                ' ❤️🧡💛💚💙💜🖤'
                '</span></h2>',unsafe_allow_html=True)

    help.newLine(lines=3)

    st.markdown('<h2 style="text-align:center;"> <span style="color:#F633FF"> Make sure you have enough Peter André '
                'in your life <br><br>Upload a pic and see if Pete is in it!'
                '</span> 👏 </h2> ', unsafe_allow_html=True)

    help.newLine(lines=3)

    #picture = st.file_uploader(label='Picture goes here')

    picture = st.file_uploader(label='Picture goes here', type=['png', 'jpg', 'jpeg'])
    if picture is not None:


        #image = Image.read(picture)
        img = Image.open(picture)
        image = np.asarray(img)


        # DETECT FACES

        detector = Detection.get_detector()
        img_faces = Detection.extract_face_from_image(image, detector)

        petes = Detection.get_petes(detector)
        boolean = Detection.find_pete(petes, image, detector)

        fig = Detection.highlight_faces_bool(image, detector, boolean)

        if len(img_faces) > 1:
            st.markdown('<h2 style="text-align:center;"> There are <span style="color:#F633FF"> {} </span> '
                        'faces in '
                        'your picture! </h2> '.format(len(img_faces)), unsafe_allow_html=True)

        if len(img_faces) == 1:
            st.markdown('<h2 style="text-align:center;"> There is <span style="color:#F633FF"> {} </span> '
                        'face in '
                        'your picture! </h2> '.format(len(img_faces)), unsafe_allow_html=True)


        # extracted_faces = extract_face_from_image(image, faces)
        if len([x for x in boolean if x is True]) > 0:
            st.markdown('<h2 style="text-align:center;"> AND <span style="color:#FFCD33"> {} </span> '
                        'IS OF PETEEEEYYYY!!!</h2> '.format(len([x for x in boolean if x is True])), unsafe_allow_html=True)
        else:
            st.markdown('<h2 style="text-align:center;"> ..and  <span style="color:blue"> none </span> '
                        'is of Pete. Boo. That picture sucks.<h2> ', unsafe_allow_html=True)

        st.pyplot(fig)

        if len([x for x in boolean if x is True]) > 0:
            st.balloons()


if __name__ == "__main__":
    main()
