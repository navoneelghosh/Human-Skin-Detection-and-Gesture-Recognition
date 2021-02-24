# Human Skin Detection and Gesture Recognition
<html>

<body>
    <p>
        This is done as a part of the CS585 - Image and Video Computation coursework at Boston University. <br>
        Navoneel Ghosh <br>
        Date - 02/17/2021
    </p>
    <div class="main-body">
        <hr>
        <h2>
            Overall Description
        </h2>
        <p>
            Computer vision techniques were used to recognize American Sign Language alphabets in a video stream.
            Although, for now, it can only detect "L","U","C" and "K".
            Uses OpenCV.
        </p>
        <hr>
        <h2>
            Method and Implementation
        </h2>
        <p>
        <ul>
            <li>Background subtraction to perform motion segmentation.</li>
            <li>Perform median blur with kernel size 3 to remove isolated white pixels from the background.</li>
            <li>Perform gaussian blur and dilation of image further. Performing this step ensures that the palm which would be invisible due to small movements and background subtraction is now filled.</li>
            <li>Merge it with skin detection algorithm so that other stationary objects detected as skin in the background are removed.</li>
            <li>Perform multiscale template matching and display that in UI.</li>
        </ul>    
        </p>
        <hr>
        <h2>Experiments</h2>
        <p>
            A confusion matrix has been created from 97 frames of one of the videos of the gesture detection. </p>
        <p>
        <table>
            <tbody>
                <tr>
                    <td colspan="8">
                        <center>
                            <h3>Confusion Matrix</h3>
                        </center>
                    </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> </td>
                    <td> </td>
                    <td> Truth </td>
                    <td> </td>
                    <td> </td>
                    <td> </td>
                    <td> </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> </td>
                    <td> "L" </td>
                    <td> "U" </td>
                    <td> "C" </td>
                    <td> "K" </td>
                    <td> Prediction Sum </td>
                    <td> Precision </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> "L" </td>
                    <td> 14 </td>
                    <td> 0 </td>
                    <td> 0 </td>
                    <td> 0 </td>
                    <td> 14 </td>
                    <td> 100% </td>
                </tr>
                <tr>
                    <td> Prediction </td>
                    <td> "U" </td>
                    <td> 0 </td>
                    <td> 23 </td>
                    <td> 0 </td>
                    <td> 10 </td>
                    <td> 33 </td>
                    <td> 69.69% </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> "C" </td>
                    <td> 3 </td>
                    <td> 6 </td>
                    <td> 21 </td>
                    <td> 6 </td>
                    <td> 36 </td>
                    <td> 58.33% </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> "K" </td>
                    <td> 0 </td>
                    <td> 0 </td>
                    <td> 0 </td>
                    <td> 14 </td>
                    <td> 14 </td>
                    <td> 100% </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> Truth Sum </td>
                    <td> 17 </td>
                    <td> 29 </td>
                    <td> 21 </td>
                    <td> 30 </td>
                    <td> 97 </td>
                    <td> </td>
                </tr>
                <tr>
                    <td> </td>
                    <td> Recall </td>
                    <td> 82.35% </td>
                    <td> 79.31% </td>
                    <td> 100% </td>
                    <td> 46.67% </td>
                    <td> </td>
                    <td> </td>
                </tr>
            </tbody>
        </table>
        </p>
        <br>
        <p>
            Accuracy = 74.23%
        </p>
        <hr>
        <h2>Results</h2>
        https://drive.google.com/file/d/1m84Q-sv3jZJDXuVSTmjwynWaY8OrMGRd/preview
        <hr>
    </div>
</body>


</html>