from Faces import Detection
from Utils import help
import streamlit as st
from PIL import Image
import numpy as np
import base64


def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    st.markdown('<h2 style="text-align:center;"> Make sure you have enough Peter André '
                'in your life <br><br>Upload a pic and see if Pete is in it!'
                ' 👏 </h2> ', unsafe_allow_html=True)



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
            st.markdown('<h2 style="text-align:center;"> and {} '
                        'is if Pete!</h2> '.format(len([x for x in boolean if x is True])), unsafe_allow_html=True)
        else:
            st.markdown('<h2 style="text-align:center;"> ..and none '
                        'is of Pete. Boo. You should reconsider your taste in pictures.<h2> ', unsafe_allow_html=True)

        st.pyplot(fig)

        if len([x for x in boolean if x is True]) > 0:
            st.balloons()


if __name__ == "__main__":
    main()
