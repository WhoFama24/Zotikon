<!doctype html>
<html>
	<head>
		<meta charset="utf-8">
		<meta name="keywords" content="bootstrap theme, bootstrap template, html5 theme">
		<meta name="description" content="Mississippi State University - CPE Senior Design - Zotikon Project">
		<link rel="shortcut icon" type="image/png" href="favicon.png"/>
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0">
		<link rel="stylesheet" type="text/css" href="./css/bootstrap.css">
		<link rel="stylesheet" type="text/css" href="./style.css">
		<link rel="stylesheet" href="./css/animate.css"/>
		<script src="./js/jquery-2.1.0.js"></script>
		<script src="./js/bootstrap.js"></script>
		<script src="./js/typer.js"></script>
		<script src="./js/blocs.js"></script>
		<link rel='stylesheet' href='./css/et-line.min.css'/>
		<link rel='stylesheet' href='./css/font-awesome.min.css'/>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"rel="stylesheet">
		<title>Zotikon Project</title>
	</head>
	<body>
		<!-- Main container -->
		<div class="page-container">
			<!-- Navigation Bloc -->
			<div class="bloc bgc-nav-bar d-bloc" id="nav-bloc">
				<div class="container">
					<nav class="navbar row">
						<div class="navbar-header">
							<a class="navbar-brand tc-white" href="index.html"><span class="et-icon-rss icon-sm icon-white zoomIn animated tc-white"></span> Zotikon</a>
							<button id="nav-toggle" type="button" class="ui-navbar-toggle navbar-toggle" data-toggle="collapse"
								data-target=".navbar-1">
							<span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span
								class="icon-bar"></span><span class="icon-bar"></span>
							</button>
						</div>
						<div class="collapse navbar-collapse navbar-1">
							<ul class="site-navigation nav navbar-nav">
								<li>
									<a  onclick="scrollToTarget('#introduction')">Introduction</a>
								</li>
								<li>
									<a  onclick="scrollToTarget('#deliverables')">Deliverables</a>
								</li>
								<li>
									<a onclick="scrollToTarget('#team')">Team</a>
								</li>
								<li>
									<a onclick="scrollToTarget('#gallery')">Gallery</a>
								</li>
								<li>
									<a onclick="scrollToTarget('#datasheets')">Datasheets</a>
								</li>
								<li>
									<a onclick="scrollToTarget('#source-code')">Source Code</a>
								</li>
							</ul>
						</div>
					</nav>
				</div>
			</div>
			<!-- Navigation Bloc END -->
			<!-- header -->
			<div class="bloc  bg-city-overlay d-bloc" id="header">
				<div class="container bloc-xl">
					<div class="row">
						<div class="col-sm-12">
							<h3 class="text-center mg-lg tc-white">Zotikon</h3>
							<p class="dis-item text-center tc-white animated fadeInUp animDelay02">
								Athlete Analysis System
							</p>
							<div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-platinum animDelay06 animated fadeInUp"
									onclick="scrollToTarget('#deliverables')">Deliverables</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!-- header END -->
			<!-- introduction -->
			<div class="bloc l-bloc bgc-white" id="introduction">
				<div class="container bloc-md">
                    <div class="row mg-md">
                        <div class="col-md-12">
                            <h2 class="text-center mg-md">Introduction</h2>
                            <hr>
                            <div class="col-xs-12 col-md-6">
                                <img id="product-spec-img" src="img/Zotikon_ProductSpecification_Final_NoBackground.png" alt="Product Specification" class="img-responsive">
                            </div>
                            <div id="product-spec-img-modal" class="modal">
                                <span class="close">&times;</span>
                                <img class="modal-content" id="product-spec-modal-img">
                                <div id="caption"></div>
                            </div>
                            <div class="col-xs-12 col-md-6">
                                <p>
                                    Professional trainers for competitive athletes continually seek to improve athlete performance during training and competition but lack
                                    the ability to conveniently and accurately monitor the essential performance indicators or a method to analyze performances post-exercise.
                                    Zotikon provides real-time monitoring of those indicators and communicates them through a robust network to trainers to allow for advanced,
                                    adaptive workouts and finely-tuned recovery periods and, upon completion of the exercise, the information is available in common data formats
                                    for further analysis.
                                </p>
                                <p>
                                    The Zotikon system is composed of two subsystems: the athlete-worn device and the trainer station. The athlete-worn device collects the
                                    essential indicators about the athlete in real time and transmits it to the trainer station for monitoring purposes. The Zotikon system
                                    assists athletes and trainers by providing real-time data monitoring on athletes while they perform. The athlete-worn device collects
                                    the heart rate and temperature of the athlete, stores those measurements in a small internal memory until a transmission window arrives,
                                    and transmits the measurements to the monitoring station using the mesh network inherent to Synapse devices. The monitoring station
                                    continuously polls the athlete-worn devices for new measurements and stores those measurements into a time-series database. The web
                                    server running on the monitoring station provides a single-page application to the client, where the training staff views the information.
                                </p>
                            </div>
                        </div>
                    </div>
				</div>
			</div>
			<!-- introduction END -->
			<!-- deliverables -->
            <div class="bloc bgc-outer-space d-bloc" id="deliverables">
				<div class="container bloc-md">
					<div class="row">
						<div class="col-sm-12">
							<h2 class="text-center mg-md ">Deliverables</h2>
							<table>
								<thead>
									<tr>
										<th>Document</th>
										<th>Rough Draft</th>
										<th colspan="2">Final Draft</th>
									</tr>
								</thead>
								<tbody>
                                    <tr>
										<td>Product Specification</td>
										<td><a href="deliverables/Zotikon_ProductSpecification_Draft.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
                                        <td></td>
										<td><a href="deliverables/Zotikon_ProductSpecification_Final.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
									</tr>
									<tr>
                                        <td>Problem Statement</td>
										<td><a href="deliverables/Zotikon_ProblemStatement_Draft.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
										<td><a href="deliverables/Zotikon_ProblemStatement_Final.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
                                        <td><a href="deliverables/Zotikon_ProblemStatement_Final.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
									</tr>
									<tr>
										<td>Design Constraints</td>
										<td><a href="deliverables/Zotikon_DesignConstraints_Draft.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
										<td><a href="deliverables/Zotikon_DesignConstraints_Final.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
                                        <td><a href="deliverables/Zotikon_DesignConstraints_Final.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
									</tr>
									<tr>
										<td>Approach</td>
										<td><a href="deliverables/Zotikon_Approach_Draft.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
										<td><a href="deliverables/Zotikon_Approach_Final.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
                                        <td><a href="deliverables/Zotikon_Approach_Final.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
									</tr>
                                    <tr>
										<td>Mid-Semester Presentation</td>
										<td><a href="deliverables/Zotikon_MidSemesterPresentation_Draft.pptx" target="_blank"><span class="fa fa-file-powerpoint-o"></span></a></td>
										<td><a href="deliverables/Zotikon_MidSemesterPresentation_Final.pptx" target="_blank"><span class="fa fa-file-powerpoint-o"></span></a></td>
                                        <td><a href="deliverables/Zotikon_MidSemesterPresentation_Final.pdf" target="_blank"><span class="fa fa-file-pdf-o"></span></a></td>
									</tr>
                                    <tr>
										<td>Executive Summary</td>
										<td><a href="deliverables/Zotikon_ExecutiveSummary_Draft.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
										<td></td>
                                        <td></td>
									</tr>
                                    <tr>
										<td>Evaluation</td>
										<td><a href="deliverables/Zotikon_Evaluation_Draft.docx" target="_blank"><span class="fa fa-file-word-o"></span></a></td>
										<td></td>
                                        <td></td>
									</tr>
                                    <tr>
										<td>Final Presentation</td>
										<td><a href="deliverables/Zotikon_FinalPresentation_Draft.pptx" target="_blank"><span class="fa fa-file-powerpoint-o"></span></a></td>
										<td></td>
                                        <td></td>
									</tr>
                                    <tr>
										<td>Schematics</td>
										<td></td>
										<td></td>
                                        <td></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
			<!-- deliverables END -->
			<!-- team -->
            <div class="bloc l-bloc bgc-white" id="team">
				<div class="container bloc-sm">
					<div class="row">
						<div class="col-sm-12">
							<h2 class="text-center mg-md ">
								Zotikon Team Members
                            </h2>
						</div>
					</div>
					<div class="row voffset-lg">
                        <div class="col-sm-1">
                            <!-- This div is here to center the pictures on the page -->
                        </div>
						<div class="col-sm-2">
							<img src="img/Bowlin,%20Bruce%20-%20Profile%20Picture.png" class="img-responsive animated zoomIn" alt="member"/>
							<h3 class="text-center mg-md">
								Bruce Bowlin
							</h3>
							<p class="text-center">
								Wireless System Lead
							</p>
                            <p class="text-center">
								Heart Rate System
							</p>
                            <div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-outer-space animated fadeInUp"
									href="team/resumes/bruce_bowlin.pdf" target="_blank">Resume</a>
							</div>
						</div>
						<div class="col-sm-2">
							<img src="img/Farmer,%20Eric%20-%20Profile%20Picture.png" class="img-responsive animated zoomIn animDelay02" alt="member"/>
							<h3 class="text-center mg-md">
								Eric Farmer
							</h3>
							<p class="text-center">
								Team Leader
							</p>
                            <p class="text-center">
								Monitoring Station Lead
							</p>
                            <p class="text-center">
								Temperature System
							</p>
                            <div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-outer-space animDelay02 animated fadeInUp"
									href="team/resumes/Resume_EricFarmer.pdf" target="_blank">Resume</a>
							</div>
						</div>
						<div class="col-sm-2">
							<img src="img/Hastings,%20Joseph%20-%20Profile%20Picture.png" class="img-responsive animDelay04 animated zoomIn" alt="member"/>
							<h3 class="text-center mg-md">
								Joseph Hastings
							</h3>
							<p class="text-center">
								Power Systems Lead
							</p>
                            <p class="text-center">
								Heart Rate System
							</p>
                            <div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-outer-space animDelay04 animated fadeInUp"
									href="team/resumes/Resume_JosephHastings.pdf" target="_blank">Resume</a>
							</div>
						</div>
						<div class="col-sm-2">
							<img src="img/Kingma,%20Van%20-%20Profile%20Picture.png" class="img-responsive animDelay06 animated zoomIn" alt="member"/>
							<h3 class="text-center mg-md">
								Van Kingma
							</h3>
							<p class="text-center">
								Temperature System Lead
							</p>
                            <p class="text-center">
                                Wireless System
							</p>
                            <div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-outer-space animDelay06 animated fadeInUp"
									href="team/resumes/van_kingma.pdf" target="_blank">Resume</a>
							</div>
						</div>
                        <div class="col-sm-2">
							<img src="img/Prehn,%20Curtis%20-%20Profile%20Picture.png" class="img-responsive animDelay08 animated zoomIn" alt="member"/>
							<h3 class="text-center mg-md">
								Curtis Prehn
							</h3>
							<p class="text-center">
								Heart Rate System Lead
							</p>
                            <p class="text-center">
								Power Systems
							</p>
                            <div class="text-center">
								<a class="btn  btn-md btn-wire wire-btn-outer-space animDelay08 animated fadeInUp"
									href="team/resumes/Resume_CurtisPrehn.pdf" target="_blank">Resume</a>
							</div>
						</div>
					</div>
				</div>
			</div>
			<!-- team END -->
			<!-- gallery -->
            <div class="bloc bgc-outer-space d-bloc" id="gallery">
				<div class="container bloc-lg">
					<div class="row">
						<div class="col-sm-12">
							<h2 class="text-center mg-md ">
								Photo Gallery
							</h2>
							<p class="text-center sub-heading">
								Photo documentation of the Zotikon system.
							</p>
						</div>
					</div>
					<div class="row voffset">
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/Zotikon_ProductSpecification_Final.png" data-caption="Zotikon Problem Specification & Overview">
                                <img src="img/Zotikon_ProductSpecification_Final.png" class="img-responsive animated zoomIn" alt="portfolio"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/Zotikon_FunctionalityDiagram.png" data-caption="Zotikon Operational Overview"><img
								src="img/Zotikon_FunctionalityDiagram.png" class="img-responsive animated zoomIn" alt="portfolio"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/Zotikon_SystemOverview.png" data-caption="Zotikon System Overview"><img
								src="img/Zotikon_SystemOverview.png" class="img-responsive animated zoomIn" alt="portfolio"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/Zotikon_ProjectSchedule.png" data-caption="Zotikon Project Schedule"><img
								src="img/Zotikon_ProjectSchedule.png" class="img-responsive animated zoomIn" alt="portfolio"/></a>
						</div>
					</div>
					<div class="row voffset">
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/Zotikon_DatabaseDesign.png" data-caption="Zotikon - Monitoring Station Database Design"><img
								src="img/Zotikon_DatabaseDesign.png" class="img-responsive animDelay04 animated zoomIn" alt="portfolio"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="" data-caption="Image description"><img
								src="" class="img-responsive animated zoomIn animDelay04" alt="TODO"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="img/work-11.jpg" data-caption="Image description"><img
								src="" class="img-responsive animDelay04 animated zoomIn" alt="TODO"/></a>
						</div>
						<div class="col-sm-3">
							<a href="#" data-lightbox="" data-caption="Image description"><img
								src="" class="animDelay04 animated zoomIn img-responsive" alt="TODO"/></a>
						</div>
					</div>
				</div>
			</div>

			<!-- gallery END -->
			<!-- datasheets -->
			<div class="bloc l-bloc bgc-white" id="datasheets">
				<div class="container bloc-md">
					<div class="row">
						<div class="col-sm-12">
							<h2 class="text-center mg-md ">Datasheets</h2>
                            <p class="text-center sub-heading">
                                The table below contains a list to the datasheets for all components in the Zotikon system.  The Digikey link
                                is also provided for direct access to the distributor site.
                            </p>
                            <p class="text-center">
                                TODO: More datasheets will be added for specific resistors and capacitors once those selections are finalized.
                            </p>
							<table>
								<thead>
									<tr>
										<th class="text-center">Component</th>
										<th class="text-center">Component Manufacturer &amp; P/N</th>
										<th class="text-center">Datasheet Link</th>
                                        <th class="text-center">Digikey Link</th>
									</tr>
								</thead>
								<tbody>
                                    <tr>
										<td class="text-center">Radio/MCU</td>
										<td class="text-center">Synapse SM200</td>
										<td class="text-center"><a href="datasheets/sm220-datasheet.pdf" target="_blank"><span class="fa fa-file-pdf-o icon-sm icon-white"></span></a></td>
                                        <td class="text-center"><a href="https://www.digikey.com/products/en?keywords=746-1031-1-ND" target="_blank">746-1031-1-ND</a></td>
									</tr>
									<tr>
                                        <td class="text-center">Instrumentation Amplifier</td>
										<td class="text-center">Analog Devices AD623ANZ</td>
										<td class="text-center"><a href="datasheets/AD_AD623ANZ_Instrumentation_Amplifier.pdf" target="_blank"><span class="fa fa-file-pdf-o icon-sm icon-white"></span></a></td>
                                        <td class="text-center"><a href="https://www.digikey.com/products/en?keywords=AD623ANZ" target="_blank">AD623ANZ-ND</a></td>
									</tr>
									<tr>
										<td class="text-center">Temperature Sensor - Infrared</td>
										<td class="text-center">Melexis MLX90615</td>
										<td class="text-center"><a href="datasheets/MLX90615-Datasheet-Melexis.pdf" target="_blank"><span class="fa fa-file-pdf-o icon-sm icon-white"></span></a></td>
                                        <td class="text-center"><a href="https://www.digikey.com/product-detail/en/melexis-technologies-nv/MLX90615SSG-DAA-000-TU/MLX90615SSG-DAA-000-TU-ND/2440563" target="_blank">MLX90615SSG-DAA-000-TU-ND</a></td>
									</tr>
									<tr>
										<td class="text-center">Temperature Sensor - Contact</td>
										<td class="text-center">Maxim Integrated DS1631</td>
										<td class="text-center"><a href="datasheets/DS1631_Datasheet.pdf" target="_blank"><span class="fa fa-file-pdf-o icon-sm icon-white"></span></a></td>
										<td class="text-center"><a href="https://www.digikey.com/product-detail/en/maxim-integrated/DS1631U-T-R/DS1631U-T-RCT-ND/4895452" target="_blank">DS1631U+T&amp;RCT-ND</a></td>
									</tr>
									<tr>
										<td class="text-center">Monitoring Station USB Adapter</td>
										<td class="text-center">Synapse SN220</td>
										<td class="text-center"><a href="datasheets/SNAPstick_220_PB_August2016.pdf" target="_blank"><span class="fa fa-file-pdf-o icon-sm icon-white"></span></a></td>
                                        <td class="text-center"><a href="https://www.digikey.com/products/en?keywords=Synapse%20SN220" target="_blank">746-1094-ND</a></td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
			<!-- datasheets END -->
			<!-- source code -->
			<div class="bloc d-bloc bgc-outer-space" id="source-code">
				<div class="container bloc-lg">
					<div class="row">
						<div class="col-sm-12">
							<h2 class="text-center mg-md ">
								Source Code
							</h2>
							<p class="text-center sub-heading">
								The source code for the Zotikon project is available on GitHub.  The repository is tagged for release after the Fall 2017 semester of senior design
                                and after the Spring 2018 semester of senior design.  The commands below show how to clone the repository for a specific release.
							</p>
						</div>
					</div>
                    <div class="row">
                        <pre>
                            // Clone Latest Repository
                            https://github.com/WhoFama24/zotikon.git</pre>
                        <pre>
                            // Clone Fall Semester 2017 Release
                            https://github.com/WhoFama24/zotikon.git --branch fall17_release</pre>
                        <pre>
                            // Clone Spring Semester 2018 Release
                            https://github.com/WhoFama24/zotikon.git --branch spring18_release</pre>
                    </div>
				</div>
			</div>
			<!-- source-code END -->
			<!-- ScrollToTop Button -->
			<a class="bloc-button btn btn-d scrollToTop" onclick="scrollToTarget('1')"><span
				class="fa fa-chevron-up"></span></a>
			<!-- ScrollToTop Button END-->
			<!-- Footer - bloc-8 -->
			<div class="bloc bgc-platinum l-bloc" id="bloc-8">
				<div class="container bloc-sm">
					<div class="row">
						<p class="text-center">
                            <a href="#header">Home</a> |
                            <a href="https://sites.google.com/site/msueceseniordesign/Home">MsState CPE 4532 Homepage</a> |
                            <a href="https://sites.google.com/site/msueceseniordesign/project-list">MsState Senior Design Projects Page</a> |
                            <a href="http://www.ece.msstate.edu/">MsState ECE Department Main Page</a>
                        </p>
                        <p class="text-center">
                            © Copyright Team Zotikon 2017
                        </p>
					</div>
				</div>
			</div>
			<!-- Footer - bloc-8 END -->
		</div>
		<!-- Main container END -->
	</body>
	<!-- Google Analytics -->
	<!-- Google Analytics END -->

    <script>
        var modal = document.getElementById('product-spec-img-modal');
        var img = document.getElementById('product-spec-img');
        var modalImg = document.getElementById('product-spec-modal-img');
        var captionText = document.getElementById('caption');

        img.onclick = function() {
            modal.style.display = "block";
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        }

        var span = document.getElementsByClassName('close')[0];
        span.onclick = function() {
            modal.style.display = "none";
        }

        modal.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }
    </script>
</html>
