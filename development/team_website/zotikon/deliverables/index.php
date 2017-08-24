<!DOCTYPE html>
<html>
    <head>
        <meta chars="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        
        <title>Zotikon Deliverables</title>
        <meta name="description" content="Zotikon Deliverables Page">
        <meta name="author" content="Team Zotikon">
        
        <!-- Stylesheets -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>
        <link rel="stylesheet" href="index_style.css">
    </head>
    <body>
        <nav class="navbar navbar-inverse">
            <div class="container-fluid">
                <div class="navbar-header">
                    <a class="navbar-brand" href="/../zotikon/">Zotikon</a>
                </div>
                
                <ul class="nav navbar-nav navbar-right">
                    <li><a href="/zotikon/deliverables/">Deliverables</a></li>
                    <li><a href="/../zotikon/team/">Team</a></li>
                    <li><a href="/../zotikon/gallery/">Gallery</a></li>
                    <li><a href="/../zotikon/datasheets/">Datasheets</a></li>
                    <li><a href="/../zotikon/source_code/">Source Code</a></li>
                </ul>
            </div>
        </nav>
        <h1 class="text-center">Deliverables</h1>
        <div class='container'>
            <table class="table table-hover text-center">
                <thead>
                    <tr>
                        <th class="text-center">Document</th>
                        <th class="text-center">Rough Draft</th>
                        <th class="text-center">Final Draft</th>
                    </tr>
                </thead>
                <tbody>

                    <?php
                        
                        function add_document($Document, $draft="", $final="")
                        {
                            $file_dir = getcwd()."/files/";
                            echo "
                                <tr>
                                    <td>".$Document."</td>";
                            if($draft != "")
                            {
                                echo "
                                <td>
                                        <a href='".$file_dir.$draft."' download>
                                            <span class= 'glyphicon glyphicon-download-alt' />
                                        </a>
                                    </td>";
                            } else {
                                echo "<td></td>";
                            }
                                    
                            if($final != "")
                            {
                                echo "
                                    <td>
                                        <a href='".$file_dir.$final."' download>
                                            <span class= 'glyphicon glyphicon-download-alt' />
                                        </a>
                                    </td>
                                </tr>";
                            } else {
                                echo "<td></td>";
                            }
                        }
                    
                        add_document("Problem Statement");
                        add_document("Product Specification");
                        add_document("Design Constraints");
                        add_document("Approach");
                        add_document("Mid-Semester Presentation");
                        add_document("Executive Summary");
                        add_document("Evaluation");
                        add_document("Final Presentation");
                        add_document("Final Design Document");
                        add_document("Schematics");
                    
                    ?>
                </tbody>
            </table>    
        </div>
    </body>
</html>