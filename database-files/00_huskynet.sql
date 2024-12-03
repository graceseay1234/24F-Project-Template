DROP DATABASE IF EXISTS huskynet;

CREATE DATABASE huskynet;

USE huskynet;

# ---------------------------------------------------------------------- #
# Add table "Job"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Job (
  JobID VARCHAR(50) NOT NULL,
  Title VARCHAR(75) NOT NULL,
  Description VARCHAR(1000),
  Status VARCHAR(100),
  PRIMARY KEY (JobID)

);

CREATE INDEX job_id ON Job (JobID);


# ---------------------------------------------------------------------- #
# Add table "Trait"                                              #
# ---------------------------------------------------------------------- #

CREATE TABLE Trait (
  TraitID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Description VARCHAR(1000),
  PRIMARY KEY (TraitID)

);

CREATE INDEX trait_id ON Trait (TraitID);

# ---------------------------------------------------------------------- #
# Add table "Candidate"                                              #
# ---------------------------------------------------------------------- #

CREATE TABLE Candidate (
  CandidateID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  InterviewNotes VARCHAR(1000),
  Status VARCHAR(50),
  Qualities VARCHAR(1000),
  PRIMARY KEY (CandidateID)

);

CREATE INDEX candidate_id ON Candidate (CandidateID);

# ---------------------------------------------------------------------- #
# Add table "HiringUser"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE HiringUser (
  UserID VARCHAR(50) NOT NULL,
  Name VARCHAR(50),
  Role VARCHAR(50),

  PRIMARY KEY (UserID),
  CONSTRAINT fk_user FOREIGN KEY (UserID) REFERENCES Job(JobID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_user FOREIGN KEY (UserID) REFERENCES Candidate(CandidateID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX users_id ON HiringUser (UserID);

# ---------------------------------------------------------------------- #
# Add table "Engagement"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Engagement (
  EngagementID VARCHAR(50) NOT NULL,
  ConnectionsReq VARCHAR(50),
  ActiveUserCount INT,
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (EngagementID)
);

CREATE INDEX engagement_id ON Engagement (EngagementID);

# ---------------------------------------------------------------------- #
# Add table "Feedback"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Feedback (
  FeedbackID VARCHAR(50) NOT NULL,
  Content VARCHAR(2000),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (FeedbackID)
);

CREATE INDEX feedback_id ON Feedback (FeedbackID);


# ---------------------------------------------------------------------- #
# Add table "PerformanceMetrics"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE PerformanceMetrics (
  MetricID VARCHAR(50) NOT NULL,
  ResponseTime TIME,
  UpTime TIME,
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (MetricID),
  CONSTRAINT fk_metrics FOREIGN KEY (MetricID) REFERENCES Engagement(EngagementID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX metric_id ON PerformanceMetrics(MetricID);


# ---------------------------------------------------------------------- #
# Add table "Feature"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Feature (
  FeatureID VARCHAR(50) NOT NULL,
  Name VARCHAR(2000),
  UserCount INT,
  PRIMARY KEY (FeatureID),
  CONSTRAINT fk_feature FOREIGN KEY (FeatureID) REFERENCES PerformanceMetrics(MetricID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_feature FOREIGN KEY (FeatureID) REFERENCES Feedback(FeedbackID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX feature_id ON Feature (FeatureID);

# ---------------------------------------------------------------------- #
# Add table "AnalyticsUser"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE AnalyticsUser (
  UserID VARCHAR(50) NOT NULL,
  Location VARCHAR(50),
  Major VARCHAR(50),

  PRIMARY KEY (UserID),
  CONSTRAINT fk_anauser FOREIGN KEY (UserID) REFERENCES Feedback(FeedbackID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_anauser FOREIGN KEY (UserID) REFERENCES Feature(FeatureID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk3_anauser FOREIGN KEY (UserID) REFERENCES Engagement(EngagementID)
  ON UPDATE cascade ON DELETE restrict
);

CREATE INDEX anausers_id ON AnalyticsUser (UserID);

# ---------------------------------------------------------------------- #
# Add table "SearchFilters"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE SearchFilters (
  FilterID VARCHAR(50) NOT NULL,
  FilterType VARCHAR(50),
  PRIMARY KEY (FilterID)
);

CREATE INDEX filter_id ON SearchFilters(FilterID);


# ---------------------------------------------------------------------- #
# Add table "Skills"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Skills (
  SkillID VARCHAR(50) NOT NULL,
  SkillName VARCHAR(200),
  AlumniID INT,
  PRIMARY KEY (SkillID)

);

CREATE INDEX skills_id ON Skills(SkillID);

# ---------------------------------------------------------------------- #
# Add table "Messages"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Messages (
  MessageID VARCHAR(50) NOT NULL,
  SenderAlumniID INT,
  ReceiverAlumniID INT,
  MessageContent VARCHAR(2000),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (MessageID)

);

CREATE INDEX msgs_id ON Messages(MessageID);

# ---------------------------------------------------------------------- #
# Add table "WorkExperience"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE WorkExperience (
  ExperienceID VARCHAR(50) NOT NULL,
  AlumniID INT,
  Role VARCHAR(50),
  Company VARCHAR(50),
  StartDate DATE,
  EndDate DATE,
  IsCurrent BOOLEAN,
  PRIMARY KEY (ExperienceID)

);

CREATE INDEX work_id ON WorkExperience(ExperienceID);

# ---------------------------------------------------------------------- #
# Add table "Actions"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Actions (
  ActionID VARCHAR(50) NOT NULL,
  AlumniID INT,
  AdminID INT,
  ActionType VARCHAR(50),
  ActionTS datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (ActionID)

);

CREATE INDEX action_id ON Actions(ActionID);

# ---------------------------------------------------------------------- #
# Add table "Warnings"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Warnings (
  WarningID VARCHAR(50) NOT NULL,
  AlumniID INT,
  AdminID INT,
  Reason VARCHAR(500),
  TimeStamp datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
  PRIMARY KEY (WarningID)

);

CREATE INDEX warn_id ON Warnings(WarningID);

# ---------------------------------------------------------------------- #
# Add table "Administrator"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Administrator (
  AdminID VARCHAR(50) NOT NULL,
  Name VARCHAR(50),
  Email VARCHAR(100),
  Role VARCHAR(100),
  PRIMARY KEY (AdminID),
  CONSTRAINT fk_admin FOREIGN KEY (AdminID) REFERENCES Warnings(WarningID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk2_admin FOREIGN KEY (AdminID) REFERENCES Actions(ActionID)
  ON UPDATE cascade ON DELETE restrict

);

CREATE INDEX admin_id ON Administrator(AdminID);


# ---------------------------------------------------------------------- #
# Add table "Alumni"                                                      #
# ---------------------------------------------------------------------- #

CREATE TABLE Alumni (
  AlumniID VARCHAR(50) NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Major VARCHAR(50) NOT NULL,
  AboutMe VARCHAR(2000),
  ProfilePic VARCHAR(2000),
  WorkExperience VARCHAR(2000),
  GradYear INT,
  PRIMARY KEY (AlumniID),
  CONSTRAINT fk2_alumni FOREIGN KEY (AlumniID) REFERENCES Messages(MessageID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk3_alumni FOREIGN KEY (AlumniID) REFERENCES WorkExperience(ExperienceID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk4_alumni FOREIGN KEY (AlumniID) REFERENCES Actions(ActionID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk5_alumni FOREIGN KEY (AlumniID) REFERENCES Warnings(WarningID)
  ON UPDATE cascade ON DELETE restrict

);

CREATE INDEX alumni_id ON Alumni(AlumniID);


#Bridge tables
# ---------------------------------------------------------------------- #
# Add table "Candidate_Traits"                                           #
# ---------------------------------------------------------------------- #

CREATE TABLE Candidate_Traits (
  CandidateID VARCHAR(50) NOT NULL,
  TraitID VARCHAR(50) NOT NULL,
  CONSTRAINT ct_pk PRIMARY KEY(CandidateID, TraitID),
  CONSTRAINT fk_ct FOREIGN KEY (CandidateID) REFERENCES Candidate(CandidateID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_ct2 FOREIGN KEY (TraitID) REFERENCES Trait(TraitID)
  ON UPDATE cascade ON DELETE restrict
);

# ---------------------------------------------------------------------- #
# Add table "Alumni_Skills"                                           #
# ---------------------------------------------------------------------- #

CREATE TABLE Alumni_Skills (
  AlumniID VARCHAR(50) NOT NULL,
  SkillsID VARCHAR(50) NOT NULL,
  CONSTRAINT as_pk PRIMARY KEY(AlumniID, SkillsID),
  CONSTRAINT fk_as FOREIGN KEY (AlumniID) REFERENCES Alumni(AlumniID)
  ON UPDATE cascade ON DELETE restrict,
  CONSTRAINT fk_as2 FOREIGN KEY (SkillsID) REFERENCES Skills(SkillID)
  ON UPDATE cascade ON DELETE restrict
);

###Begin inserting mock data

insert into Job (JobID, Title, Description, Status) values (1, 'Chief Design Engineer', 'Centralized discrete instruction set', 'inactive');
insert into Job (JobID, Title, Description, Status) values (2, 'Media Manager IV', 'Public-key dedicated synergy', 'active');
insert into Job (JobID, Title, Description, Status) values (3, 'Internal Auditor', 'Inverse multi-tasking extranet', 'inactive');
insert into Job (JobID, Title, Description, Status) values (4, 'Research Nurse', 'Multi-layered logistical toolset', 'active');
insert into Job (JobID, Title, Description, Status) values (5, 'Account Coordinator', 'Implemented context-sensitive customer loyalty', 'inactive');
insert into Job (JobID, Title, Description, Status) values (6, 'Research Assistant IV', 'Proactive national algorithm', 'active');
insert into Job (JobID, Title, Description, Status) values (7, 'Administrative Officer', 'User-centric analyzing concept', 'active');
insert into Job (JobID, Title, Description, Status) values (8, 'Legal Assistant', 'Function-based foreground infrastructure', 'active');
insert into Job (JobID, Title, Description, Status) values (9, 'Cost Accountant', 'Visionary 5th generation time-frame', 'active');
insert into Job (JobID, Title, Description, Status) values (10, 'Financial Advisor', 'Diverse dedicated hardware', 'active');
insert into Job (JobID, Title, Description, Status) values (11, 'Programmer Analyst II', 'Fundamental holistic approach', 'inactive');
insert into Job (JobID, Title, Description, Status) values (12, 'Budget/Accounting Analyst I', 'Triple-buffered multi-state Graphical User Interface', 'inactive');
insert into Job (JobID, Title, Description, Status) values (13, 'Chemical Engineer', 'Upgradable intermediate knowledge base', 'inactive');
insert into Job (JobID, Title, Description, Status) values (14, 'Financial Advisor', 'Triple-buffered systemic instruction set', 'active');
insert into Job (JobID, Title, Description, Status) values (15, 'Web Designer IV', 'Customer-focused mission-critical function', 'inactive');
insert into Job (JobID, Title, Description, Status) values (16, 'Registered Nurse', 'User-centric client-server initiative', 'inactive');
insert into Job (JobID, Title, Description, Status) values (17, 'Administrative Officer', 'Balanced stable forecast', 'inactive');
insert into Job (JobID, Title, Description, Status) values (18, 'Budget/Accounting Analyst IV', 'Multi-channelled motivating artificial intelligence', 'active');
insert into Job (JobID, Title, Description, Status) values (19, 'Structural Analysis Engineer', 'Programmable didactic analyzer', 'inactive');
insert into Job (JobID, Title, Description, Status) values (20, 'Human Resources Assistant IV', 'Virtual exuding circuit', 'active');
insert into Job (JobID, Title, Description, Status) values (21, 'Internal Auditor', 'Synergistic 6th generation neural-net', 'active');
insert into Job (JobID, Title, Description, Status) values (22, 'Technical Writer', 'Stand-alone client-driven paradigm', 'inactive');
insert into Job (JobID, Title, Description, Status) values (23, 'Systems Administrator III', 'Versatile system-worthy project', 'active');
insert into Job (JobID, Title, Description, Status) values (24, 'Civil Engineer', 'Public-key zero administration local area network', 'active');
insert into Job (JobID, Title, Description, Status) values (25, 'Sales Associate', 'Exclusive maximized migration', 'inactive');
insert into Job (JobID, Title, Description, Status) values (26, 'Automation Specialist I', 'Face to face systematic hardware', 'inactive');
insert into Job (JobID, Title, Description, Status) values (27, 'Biostatistician III', 'Versatile mission-critical task-force', 'inactive');
insert into Job (JobID, Title, Description, Status) values (28, 'Quality Control Specialist', 'Object-based 24 hour toolset', 'inactive');
insert into Job (JobID, Title, Description, Status) values (29, 'Payment Adjustment Coordinator', 'Versatile actuating knowledge user', 'active');
insert into Job (JobID, Title, Description, Status) values (30, 'Recruiting Manager', 'Function-based uniform flexibility', 'inactive');
insert into Job (JobID, Title, Description, Status) values (31, 'Nurse', 'Digitized asymmetric alliance', 'inactive');
insert into Job (JobID, Title, Description, Status) values (32, 'Technical Writer', 'Self-enabling non-volatile neural-net', 'active');
insert into Job (JobID, Title, Description, Status) values (33, 'Help Desk Technician', 'Synchronised clear-thinking access', 'inactive');
insert into Job (JobID, Title, Description, Status) values (34, 'Clinical Specialist', 'Secured bifurcated portal', 'inactive');
insert into Job (JobID, Title, Description, Status) values (35, 'Graphic Designer', 'Focused optimal knowledge user', 'active');
insert into Job (JobID, Title, Description, Status) values (36, 'Geological Engineer', 'Operative local moderator', 'inactive');
insert into Job (JobID, Title, Description, Status) values (37, 'Associate Professor', 'Balanced executive database', 'inactive');
insert into Job (JobID, Title, Description, Status) values (38, 'Statistician III', 'Enhanced bifurcated infrastructure', 'active');
insert into Job (JobID, Title, Description, Status) values (39, 'VP Product Management', 'Triple-buffered dedicated forecast', 'inactive');
insert into Job (JobID, Title, Description, Status) values (40, 'Accountant III', 'Team-oriented multi-tasking capacity', 'inactive');

insert into Trait (TraitID, Name, Description) values (1, 'EMT Certified', 'Has a recent EMT Certificate');
insert into Trait (TraitID, Name, Description) values (2, 'Committed', 'Solid work ethics');
insert into Trait (TraitID, Name, Description) values (3, 'Detail-oriented', 'Pays attention to every detail');
insert into Trait (TraitID, Name, Description) values (4, 'Hardworking', 'Never missed a day of work');
insert into Trait (TraitID, Name, Description) values (5, 'Multilingual', 'Speaks more than one language');
insert into Trait (TraitID, Name, Description) values (6, 'Multitasker', 'Able to tackle different tasks at a time');


insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (1, 'Freemon Chansonne', 'Great past projects and qualifications', 'inactive', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (2, 'Alice Grelik', 'brought all required materials', 'inactive', 'creative thinker');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (3, 'Mozelle Ebbetts', 'Great past projects and qualifications', 'active', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (4, 'Jeffy Bestwall', 'Great past projects and qualifications', 'inactive', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (5, 'Chuck Cuschieri', 'Late to interview', 'active', 'team player');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (6, 'Courtney Harrismith', 'Not qualified for position', 'active', 'creative thinker');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (7, 'Sterne Matushenko', 'Personable and likeable', 'active', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (8, 'Correy Nicholes', 'Great past projects and qualifications', 'inactive', 'detail-oriented');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (9, 'Catlaina Studd', 'Well prepared for the interview', 'inactive', 'detail-oriented');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (10, 'Em Verman', 'brought all required materials', 'active', 'customer-focused');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (11, 'Orelie Kropp', 'brought all required materials', 'inactive', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (12, 'Caresa Jacquemy', 'Not qualified for position', 'inactive', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (13, 'Madison Standley', 'Personable and likeable', 'inactive', 'creative thinker');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (14, 'Mabel Matthesius', 'Great past projects and qualifications', 'active', 'detail-oriented');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (15, 'Hamlen Easdon', 'Personable and likeable', 'inactive', 'customer-focused');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (16, 'Coraline Durrand', 'Not qualified for position', 'inactive', 'adaptable');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (17, 'Wanda Hazelby', 'Late to interview', 'inactive', 'leadership abilities');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (18, 'Tades Coddrington', 'Great past projects and qualifications', 'inactive', 'leadership abilities');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (19, 'Waldemar Shivell', 'brought all required materials', 'active', 'team player');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (20, 'Fawnia Nibloe', 'Not qualified for position', 'active', 'leadership abilities');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (21, 'Tatiana Baitey', 'Late to interview', 'active', 'self-motivated');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (22, 'Cornie Itzik', 'Well prepared for the interview', 'inactive', 'self-motivated');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (23, 'Simonne Ayerst', 'Not qualified for position', 'inactive', 'strong communication skills');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (24, 'Dido Carbery', 'Well prepared for the interview', 'inactive', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (25, 'Clevey Ruddy', 'Well prepared for the interview', 'active', 'detail-oriented');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (26, 'Howie Indgs', 'Not qualified for position', 'inactive', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (27, 'Allie Tullett', 'Personable and likeable', 'active', 'leadership abilities');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (28, 'Brenda Jorry', 'Not qualified for position', 'inactive', 'self-motivated');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (29, 'Binni Gilyott', 'Great past projects and qualifications', 'inactive', 'leadership abilities');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (30, 'Jud Caneo', 'Personable and likeable', 'active', 'customer-focused');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (31, 'Baldwin Orrock', 'Late to interview', 'inactive', 'team player');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (32, 'Marylin Kepp', 'brought all required materials', 'active', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (33, 'Jerri Mosson', 'brought all required materials', 'active', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (34, 'Elia McKerrow', 'Well prepared for the interview', 'inactive', 'detail-oriented');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (35, 'Ely Rameau', 'Great past projects and qualifications', 'inactive', 'strong communication skills');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (36, 'Beryl Stetson', 'Not qualified for position', 'inactive', 'team player');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (37, 'Jacquenetta Biddy', 'Late to interview', 'active', 'tech-savvy');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (38, 'Raleigh Willmer', 'Late to interview', 'active', 'problem solver');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (39, 'Broderic Drewson', 'Personable and likeable', 'inactive', 'customer-focused');
insert into Candidate (CandidateID, Name, InterviewNotes, Status, Qualities) values (40, 'Merrie Huthart', 'brought all required materials', 'inactive', 'customer-focused');


insert into HiringUser (UserID, Name, Role) values (1, 'Raymund Maiden', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (2, 'Breanne Embleton', 'Staffing Consultant');
insert into HiringUser (UserID, Name, Role) values (3, 'Brice Eskell', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (4, 'Natalina Trowbridge', 'Employment Coordinator');
insert into HiringUser (UserID, Name, Role) values (5, 'Amandi Angless', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (6, 'Selle Haygreen', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (7, 'Laverna Alden', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (8, 'Dalton Haskey', 'HR Generalist');
insert into HiringUser (UserID, Name, Role) values (9, 'Deni Sawkins', 'HR Generalist');
insert into HiringUser (UserID, Name, Role) values (10, 'Alverta Digg', 'Hiring Manager');
insert into HiringUser (UserID, Name, Role) values (11, 'Korella Hume', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (12, 'Tania Korejs', 'HR Coordinator');
insert into HiringUser (UserID, Name, Role) values (13, 'Sancho Darkins', 'Talent Scout');
insert into HiringUser (UserID, Name, Role) values (14, 'Gertrude Janjusevic', 'HR Coordinator');
insert into HiringUser (UserID, Name, Role) values (15, 'Bryon Ferdinand', 'Employment Coordinator');
insert into HiringUser (UserID, Name, Role) values (16, 'Imojean Flintoff', 'Talent Scout');
insert into HiringUser (UserID, Name, Role) values (17, 'Montgomery Butterley', 'HR Coordinator');
insert into HiringUser (UserID, Name, Role) values (18, 'Caroline Kinder', 'Staffing Consultant');
insert into HiringUser (UserID, Name, Role) values (19, 'Julia Blessed', 'HR Coordinator');
insert into HiringUser (UserID, Name, Role) values (20, 'Damien Rubenfeld', 'Employment Coordinator');
insert into HiringUser (UserID, Name, Role) values (21, 'Zebulon Nend', 'Staffing Consultant');
insert into HiringUser (UserID, Name, Role) values (22, 'Matty Dunkley', 'Staffing Consultant');
insert into HiringUser (UserID, Name, Role) values (23, 'Estrellita Jacobowicz', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (24, 'Giavani Tunnow', 'Talent Acquisition Specialist');
insert into HiringUser (UserID, Name, Role) values (25, 'Joanna Kinforth', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (26, 'Granville Shearmur', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (27, 'Brandea Babe', 'Recruiter');
insert into HiringUser (UserID, Name, Role) values (28, 'Llewellyn Tuminini', 'Talent Acquisition Specialist');
insert into HiringUser (UserID, Name, Role) values (29, 'Brander Lago', 'Talent Acquisition Specialist');
insert into HiringUser (UserID, Name, Role) values (30, 'Lenora Breeder', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (31, 'Kameko Spain', 'HR Coordinator');
insert into HiringUser (UserID, Name, Role) values (32, 'Amelie Keslake', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (33, 'Helen Server', 'HR Generalist');
insert into HiringUser (UserID, Name, Role) values (34, 'Madelina Huskisson', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (35, 'Fan Etienne', 'Talent Acquisition Specialist');
insert into HiringUser (UserID, Name, Role) values (36, 'Emerson Worling', 'Talent Acquisition Specialist');
insert into HiringUser (UserID, Name, Role) values (37, 'Susi Bewsey', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (38, 'Uta Boor', 'Employment Specialist');
insert into HiringUser (UserID, Name, Role) values (39, 'Myles Schapero', 'Recruitment Coordinator');
insert into HiringUser (UserID, Name, Role) values (40, 'Dom Lamburne', 'Recruiter');

insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (1, 'server1.company.com:443', 159753, '2023-07-21 10:25:15');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (2, 'server1.company.com:443', 135789, '2024-08-06 16:58:45');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (3, 'server3.test.org:8888', 198765, '2023-06-02 08:50:02');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (4, 'server3.test.org:8888', 147852, '2024-11-18 18:32:56');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (5, '172.16.0.1:9000', 198765, '2024-01-11 01:17:23');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (6, '10.0.0.1:8000', 159753, '2023-02-26 14:34:43');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (7, '10.0.0.1:8000', 109876, '2024-03-13 12:49:58');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (8, '192.168.0.10:5000', 120987, '2023-03-23 08:47:14');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (9, '192.168.2.5:6000', 123456, '2023-04-12 23:38:45');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (10, '10.0.0.1:8000', 198765, '2024-08-02 16:36:39');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (11, '192.168.2.5:6000', 120987, '2022-10-24 21:10:40');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (12, 'server2.example.com:8081', 174369, '2023-05-19 15:33:01');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (13, '192.168.1.1:8080', 147852, '2023-01-27 06:27:20');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (14, '192.168.1.1:8080', 162534, '2022-07-10 03:00:39');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (15, 'server2.example.com:8081', 198765, '2024-02-27 04:27:32');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (16, 'server4.demo.net:9999', 198765, '2022-07-24 02:48:41');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (17, '172.16.0.1:9000', 123456, '2024-06-17 20:03:20');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (18, 'server2.example.com:8081', 135789, '2023-01-08 10:54:50');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (19, '10.10.10.1:3000', 109876, '2023-08-07 18:35:16');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (20, '192.168.2.5:6000', 198765, '2022-12-28 02:02:33');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (21, '192.168.0.10:5000', 162534, '2024-05-23 22:01:25');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (22, 'server4.demo.net:9999', 174369, '2023-01-30 09:02:46');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (23, 'server3.test.org:8888', 120987, '2023-07-24 16:10:51');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (24, '10.0.0.1:8000', 159753, '2023-10-22 05:42:37');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (25, '172.16.0.1:9000', 120987, '2024-01-17 20:28:05');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (26, 'server1.company.com:443', 162534, '2022-12-18 13:28:34');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (27, 'server1.company.com:443', 147852, '2024-07-09 02:08:00');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (28, 'server2.example.com:8081', 174369, '2024-09-13 07:08:05');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (29, '172.16.0.1:9000', 159753, '2023-04-17 18:56:03');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (30, '172.16.0.1:9000', 186243, '2024-05-03 00:03:13');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (31, '192.168.0.10:5000', 198765, '2024-03-24 05:52:45');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (32, 'server4.demo.net:9999', 147852, '2022-11-16 23:03:29');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (33, 'server1.company.com:443', 159753, '2023-07-02 16:56:59');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (34, '192.168.2.5:6000', 162534, '2023-04-09 07:07:21');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (35, '10.0.0.1:8000', 174369, '2023-05-05 14:20:12');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (36, 'server3.test.org:8888', 120987, '2023-11-14 22:33:01');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (37, 'server2.example.com:8081', 174369, '2023-09-29 19:12:44');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (38, '10.10.10.1:3000', 147852, '2024-07-29 17:02:24');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (39, '192.168.1.1:8080', 123456, '2023-02-17 03:40:51');
insert into Engagement (EngagementID, ConnectionsReq, ActiveUserCount, TimeStamp) values (40, '192.168.2.5:6000', 159753, '2022-10-07 05:00:15');


insert into Feedback (FeedbackID, Content, TimeStamp) values (1, 'The design is modern and visually appealing.', '2024-04-08 18:19:50');
insert into Feedback (FeedbackID, Content, TimeStamp) values (2, 'The design is modern and visually appealing.', '2023-05-15 08:29:12');
insert into Feedback (FeedbackID, Content, TimeStamp) values (3, 'a solid app with room for growth.', '2023-06-14 22:28:28');
insert into Feedback (FeedbackID, Content, TimeStamp) values (4, 'Overall', '2022-11-25 18:58:55');
insert into Feedback (FeedbackID, Content, TimeStamp) values (5, 'Needs improvement in terms of speed and performance.', '2023-01-16 21:36:41');
insert into Feedback (FeedbackID, Content, TimeStamp) values (6, 'Would recommend this app to others.', '2023-03-23 05:21:49');
insert into Feedback (FeedbackID, Content, TimeStamp) values (7, 'please fix this issue.', '2022-07-14 05:07:26');
insert into Feedback (FeedbackID, Content, TimeStamp) values (8, 'Would recommend this app to others.', '2023-03-04 04:15:22');
insert into Feedback (FeedbackID, Content, TimeStamp) values (9, 'I love the new features added in the latest update.', '2024-05-12 02:40:40');
insert into Feedback (FeedbackID, Content, TimeStamp) values (10, 'The design is modern and visually appealing.', '2024-10-20 11:09:00');
insert into Feedback (FeedbackID, Content, TimeStamp) values (11, 'User interface is clean and easy to navigate.', '2023-03-21 14:42:41');
insert into Feedback (FeedbackID, Content, TimeStamp) values (12, 'The design is modern and visually appealing.', '2024-01-21 12:26:51');
insert into Feedback (FeedbackID, Content, TimeStamp) values (13, 'The app keeps crashing', '2024-03-05 17:52:11');
insert into Feedback (FeedbackID, Content, TimeStamp) values (14, 'Overall', '2023-08-15 04:06:20');
insert into Feedback (FeedbackID, Content, TimeStamp) values (15, 'Very helpful app', '2022-07-13 16:31:01');
insert into Feedback (FeedbackID, Content, TimeStamp) values (16, 'User interface is clean and easy to navigate.', '2023-10-26 04:55:10');
insert into Feedback (FeedbackID, Content, TimeStamp) values (17, 'please fix this issue.', '2024-10-28 04:04:34');
insert into Feedback (FeedbackID, Content, TimeStamp) values (18, 'I love the new features added in the latest update.', '2023-05-10 04:09:01');
insert into Feedback (FeedbackID, Content, TimeStamp) values (19, 'I love the new features added in the latest update.', '2024-02-02 10:15:00');
insert into Feedback (FeedbackID, Content, TimeStamp) values (20, 'User interface is clean and easy to navigate.', '2023-09-27 02:12:16');
insert into Feedback (FeedbackID, Content, TimeStamp) values (21, 'Would recommend this app to others.', '2023-05-13 19:23:21');
insert into Feedback (FeedbackID, Content, TimeStamp) values (22, 'The app keeps crashing', '2023-06-02 06:34:12');
insert into Feedback (FeedbackID, Content, TimeStamp) values (23, 'a solid app with room for growth.', '2024-06-17 07:32:21');
insert into Feedback (FeedbackID, Content, TimeStamp) values (24, 'Would recommend this app to others.', '2024-07-27 11:46:34');
insert into Feedback (FeedbackID, Content, TimeStamp) values (25, 'Could use more customization options.', '2023-04-15 04:37:47');
insert into Feedback (FeedbackID, Content, TimeStamp) values (26, 'The design is modern and visually appealing.', '2023-04-29 06:05:40');
insert into Feedback (FeedbackID, Content, TimeStamp) values (27, 'Would recommend this app to others.', '2024-07-14 14:31:06');
insert into Feedback (FeedbackID, Content, TimeStamp) values (28, 'saved me a lot of time.', '2023-06-17 15:57:33');
insert into Feedback (FeedbackID, Content, TimeStamp) values (29, 'Needs improvement in terms of speed and performance.', '2024-05-22 21:48:30');
insert into Feedback (FeedbackID, Content, TimeStamp) values (30, 'Great app! Very user-friendly and intuitive.', '2022-12-15 11:35:11');
insert into Feedback (FeedbackID, Content, TimeStamp) values (31, 'Could use more customization options.', '2024-07-21 13:43:17');
insert into Feedback (FeedbackID, Content, TimeStamp) values (32, 'Could use more customization options.', '2023-03-01 01:06:48');
insert into Feedback (FeedbackID, Content, TimeStamp) values (33, 'User interface is clean and easy to navigate.', '2024-03-16 18:27:43');
insert into Feedback (FeedbackID, Content, TimeStamp) values (34, 'please fix this issue.', '2023-01-21 03:38:20');
insert into Feedback (FeedbackID, Content, TimeStamp) values (35, 'The app keeps crashing', '2024-06-05 03:35:14');
insert into Feedback (FeedbackID, Content, TimeStamp) values (36, 'Very helpful app', '2023-05-21 05:10:27');
insert into Feedback (FeedbackID, Content, TimeStamp) values (37, 'I love the new features added in the latest update.', '2023-09-17 06:49:22');
insert into Feedback (FeedbackID, Content, TimeStamp) values (38, 'a solid app with room for growth.', '2023-05-23 15:21:42');
insert into Feedback (FeedbackID, Content, TimeStamp) values (39, 'I love the new features added in the latest update.', '2023-10-16 04:29:24');
insert into Feedback (FeedbackID, Content, TimeStamp) values (40, 'saved me a lot of time.', '2024-03-11 03:16:57');


insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (1, '0:00:21', '0:01:40', '2023-10-03 11:34:12');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (2, '0:02:28', '0:02:58', '2024-04-20 05:13:07');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (3, '0:02:41', '0:04:21', '2023-06-10 07:08:18');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (4, '0:04:41', '0:02:20', '2022-07-29 00:20:53');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (5, '0:01:39', '0:02:24', '2023-04-30 16:06:15');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (6, '0:02:44', '0:04:06', '2023-07-30 03:28:22');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (7, '0:02:49', '0:03:03', '2024-03-02 06:30:36');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (8, '0:00:52', '0:02:31', '2024-06-10 15:51:34');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (9, '0:00:21', '0:02:47', '2022-11-20 08:46:12');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (10, '0:00:57', '0:01:37', '2022-12-02 07:16:24');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (11, '0:03:00', '0:01:24', '2023-04-13 22:00:25');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (12, '0:02:31', '0:03:36', '2022-10-19 11:08:57');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (13, '0:00:10', '0:02:30', '2024-02-10 10:54:31');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (14, '0:02:06', '0:02:59', '2022-10-10 12:36:10');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (15, '0:04:50', '0:01:46', '2023-01-18 10:44:22');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (16, '0:00:50', '0:02:52', '2024-05-21 20:04:57');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (17, '0:04:36', '0:04:39', '2024-10-27 11:44:31');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (18, '0:03:24', '0:01:20', '2023-04-26 08:46:45');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (19, '0:03:02', '0:02:17', '2024-11-18 10:55:47');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (20, '0:02:19', '0:04:20', '2022-08-26 00:17:12');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (21, '0:01:04', '0:03:20', '2024-05-15 04:42:10');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (22, '0:04:05', '0:01:38', '2023-05-28 22:49:06');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (23, '0:00:14', '0:04:22', '2023-12-12 21:59:35');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (24, '0:01:17', '0:00:50', '2024-02-29 10:55:46');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (25, '0:04:53', '0:01:42', '2024-04-02 19:09:00');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (26, '0:02:15', '0:04:23', '2024-09-16 09:25:35');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (27, '0:00:41', '0:02:48', '2024-08-17 03:48:12');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (28, '0:03:10', '0:00:21', '2024-05-28 09:40:49');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (29, '0:00:58', '0:01:51', '2023-08-13 17:37:16');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (30, '0:02:30', '0:01:24', '2023-11-08 09:25:51');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (31, '0:03:09', '0:02:23', '2022-12-28 07:22:37');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (32, '0:03:14', '0:01:35', '2022-09-18 10:04:57');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (33, '0:03:45', '0:01:19', '2024-11-21 06:55:19');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (34, '0:03:27', '0:02:54', '2024-10-23 01:50:47');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (35, '0:04:22', '0:03:08', '2024-06-24 11:53:22');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (36, '0:02:29', '0:04:26', '2024-05-12 21:25:16');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (37, '0:03:26', '0:00:53', '2023-06-04 13:55:36');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (38, '0:00:03', '0:02:22', '2022-06-16 06:49:32');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (39, '0:01:59', '0:02:36', '2023-11-28 10:34:21');
insert into PerformanceMetrics (MetricID, ResponseTime, UpTime, TimeStamp) values (40, '0:02:49', '0:02:33', '2023-03-21 03:27:22');


insert into Feature (FeatureID, Name, UserCount) values (1, 'Push notifications', 30549);
insert into Feature (FeatureID, Name, UserCount) values (2, 'Multi-language support', 125970);
insert into Feature (FeatureID, Name, UserCount) values (3, 'In-app purchases', 125650);
insert into Feature (FeatureID, Name, UserCount) values (4, 'Voice recognition', 198148);
insert into Feature (FeatureID, Name, UserCount) values (5, 'Offline mode', 127970);
insert into Feature (FeatureID, Name, UserCount) values (6, 'Customizable themes', 101000);
insert into Feature (FeatureID, Name, UserCount) values (7, 'Dark mode', 180799);
insert into Feature (FeatureID, Name, UserCount) values (8, 'Voice recognition', 158689);
insert into Feature (FeatureID, Name, UserCount) values (9, 'Push notifications', 100809);
insert into Feature (FeatureID, Name, UserCount) values (10, 'Augmented reality', 133506);
insert into Feature (FeatureID, Name, UserCount) values (11, 'Live chat support', 59214);
insert into Feature (FeatureID, Name, UserCount) values (12, 'Multi-language support', 109439);
insert into Feature (FeatureID, Name, UserCount) values (13, 'Augmented reality', 59840);
insert into Feature (FeatureID, Name, UserCount) values (14, 'Augmented reality', 34677);
insert into Feature (FeatureID, Name, UserCount) values (15, 'Push notifications', 124203);
insert into Feature (FeatureID, Name, UserCount) values (16, 'Push notifications', 182619);
insert into Feature (FeatureID, Name, UserCount) values (17, 'Customizable themes', 148654);
insert into Feature (FeatureID, Name, UserCount) values (18, 'Push notifications', 60279);
insert into Feature (FeatureID, Name, UserCount) values (19, 'Customizable themes', 54724);
insert into Feature (FeatureID, Name, UserCount) values (20, 'Multi-language support', 39910);
insert into Feature (FeatureID, Name, UserCount) values (21, 'Dark mode', 152832);
insert into Feature (FeatureID, Name, UserCount) values (22, 'Voice recognition', 126873);
insert into Feature (FeatureID, Name, UserCount) values (23, 'Live chat support', 194150);
insert into Feature (FeatureID, Name, UserCount) values (24, 'Voice recognition', 140825);
insert into Feature (FeatureID, Name, UserCount) values (25, 'Augmented reality', 71564);
insert into Feature (FeatureID, Name, UserCount) values (26, 'Offline mode', 196262);
insert into Feature (FeatureID, Name, UserCount) values (27, 'Offline mode', 27157);
insert into Feature (FeatureID, Name, UserCount) values (28, 'Multi-language support', 64346);
insert into Feature (FeatureID, Name, UserCount) values (29, 'Social media integration', 108562);
insert into Feature (FeatureID, Name, UserCount) values (30, 'Dark mode', 31968);
insert into Feature (FeatureID, Name, UserCount) values (31, 'Social media integration', 155186);
insert into Feature (FeatureID, Name, UserCount) values (32, 'Live chat support', 151042);
insert into Feature (FeatureID, Name, UserCount) values (33, 'Dark mode', 174912);
insert into Feature (FeatureID, Name, UserCount) values (34, 'Customizable themes', 179599);
insert into Feature (FeatureID, Name, UserCount) values (35, 'Social media integration', 22371);
insert into Feature (FeatureID, Name, UserCount) values (36, 'Live chat support', 167215);
insert into Feature (FeatureID, Name, UserCount) values (37, 'In-app purchases', 197031);
insert into Feature (FeatureID, Name, UserCount) values (38, 'Customizable themes', 158930);
insert into Feature (FeatureID, Name, UserCount) values (39, 'Multi-language support', 155658);
insert into Feature (FeatureID, Name, UserCount) values (40, 'Push notifications', 185065);


insert into AnalyticsUser (UserID, Location, Major) values (1, 'Oklahoma', 'Psychology');
insert into AnalyticsUser (UserID, Location, Major) values (2, 'North Carolina', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (3, 'Texas', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (4, 'Texas', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (5, 'California', 'Computer Science');
insert into AnalyticsUser (UserID, Location, Major) values (6, 'Missouri', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (7, 'Kentucky', 'Sociology');
insert into AnalyticsUser (UserID, Location, Major) values (8, 'California', 'Music Education');
insert into AnalyticsUser (UserID, Location, Major) values (9, 'Tennessee', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (10, 'Georgia', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (11, 'Florida', 'Art History');
insert into AnalyticsUser (UserID, Location, Major) values (12, 'Minnesota', 'Art History');
insert into AnalyticsUser (UserID, Location, Major) values (13, 'North Carolina', 'Sociology');
insert into AnalyticsUser (UserID, Location, Major) values (14, 'California', 'Environmental Science');
insert into AnalyticsUser (UserID, Location, Major) values (15, 'District of Columbia', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (16, 'Hawaii', 'Sociology');
insert into AnalyticsUser (UserID, Location, Major) values (17, 'Pennsylvania', 'Environmental Science');
insert into AnalyticsUser (UserID, Location, Major) values (18, 'Nevada', 'Environmental Science');
insert into AnalyticsUser (UserID, Location, Major) values (19, 'District of Columbia', 'Environmental Science');
insert into AnalyticsUser (UserID, Location, Major) values (20, 'District of Columbia', 'Art History');
insert into AnalyticsUser (UserID, Location, Major) values (21, 'Hawaii', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (22, 'New York', 'Environmental Science');
insert into AnalyticsUser (UserID, Location, Major) values (23, 'Louisiana', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (24, 'Pennsylvania', 'Biology');
insert into AnalyticsUser (UserID, Location, Major) values (25, 'Missouri', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (26, 'Washington', 'Sociology');
insert into AnalyticsUser (UserID, Location, Major) values (27, 'Florida', 'Sociology');
insert into AnalyticsUser (UserID, Location, Major) values (28, 'Arizona', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (29, 'Idaho', 'Business Administration');
insert into AnalyticsUser (UserID, Location, Major) values (30, 'District of Columbia', 'Computer Science');
insert into AnalyticsUser (UserID, Location, Major) values (31, 'California', 'Engineering');
insert into AnalyticsUser (UserID, Location, Major) values (32, 'Minnesota', 'Psychology');
insert into AnalyticsUser (UserID, Location, Major) values (33, 'Missouri', 'Biology');
insert into AnalyticsUser (UserID, Location, Major) values (34, 'Connecticut', 'Music Education');
insert into AnalyticsUser (UserID, Location, Major) values (35, 'Texas', 'Biology');
insert into AnalyticsUser (UserID, Location, Major) values (36, 'Pennsylvania', 'Fashion Design');
insert into AnalyticsUser (UserID, Location, Major) values (37, 'Iowa', 'Art History');
insert into AnalyticsUser (UserID, Location, Major) values (38, 'California', 'Biology');
insert into AnalyticsUser (UserID, Location, Major) values (39, 'Wisconsin', 'Computer Science');
insert into AnalyticsUser (UserID, Location, Major) values (40, 'Florida', 'Environmental Science');


insert into SearchFilters (FilterID, FilterType) values (1, 'Last updated');
insert into SearchFilters (FilterID, FilterType) values (2, 'Most active');
insert into SearchFilters (FilterID, FilterType) values (3, 'Most popular');
insert into SearchFilters (FilterID, FilterType) values (4, 'Newest');


insert into Skills (SkillID, SkillName, AlumniID) values (1, 'Microsoft Excel', 20);
insert into Skills (SkillID, SkillName, AlumniID) values (2, 'Customer Service', 34);
insert into Skills (SkillID, SkillName, AlumniID) values (3, 'Social Media Marketing', 29);
insert into Skills (SkillID, SkillName, AlumniID) values (4, 'Graphic Design', 31);
insert into Skills (SkillID, SkillName, AlumniID) values (5, 'Project Management', 18);
insert into Skills (SkillID, SkillName, AlumniID) values (6, 'Data Analysis', 3);
insert into Skills (SkillID, SkillName, AlumniID) values (7, 'Public Speaking', 4);
insert into Skills (SkillID, SkillName, AlumniID) values (8, 'Time Management', 20);
insert into Skills (SkillID, SkillName, AlumniID) values (9, 'Teamwork', 25);
insert into Skills (SkillID, SkillName, AlumniID) values (10, 'Problem Solving', 19);
insert into Skills (SkillID, SkillName, AlumniID) values (11, 'Sales', 8);
insert into Skills (SkillID, SkillName, AlumniID) values (12, 'Writing', 38);
insert into Skills (SkillID, SkillName, AlumniID) values (13, 'Leadership', 39);
insert into Skills (SkillID, SkillName, AlumniID) values (14, 'HTML/CSS', 4);
insert into Skills (SkillID, SkillName, AlumniID) values (15, 'SEO', 29);
insert into Skills (SkillID, SkillName, AlumniID) values (16, 'Photography', 7);
insert into Skills (SkillID, SkillName, AlumniID) values (17, 'Video Editing', 8);
insert into Skills (SkillID, SkillName, AlumniID) values (18, 'Event Planning', 3);
insert into Skills (SkillID, SkillName, AlumniID) values (19, 'Foreign Languages', 39);
insert into Skills (SkillID, SkillName, AlumniID) values (20, 'Web Development', 4);
insert into Skills (SkillID, SkillName, AlumniID) values (21, 'Accounting', 1);
insert into Skills (SkillID, SkillName, AlumniID) values (22, 'Research', 1);
insert into Skills (SkillID, SkillName, AlumniID) values (23, 'Email Marketing', 8);
insert into Skills (SkillID, SkillName, AlumniID) values (24, 'Networking', 5);
insert into Skills (SkillID, SkillName, AlumniID) values (25, 'Presentation Skills', 17);
insert into Skills (SkillID, SkillName, AlumniID) values (26, 'Negotiation', 24);
insert into Skills (SkillID, SkillName, AlumniID) values (27, 'Critical Thinking', 31);
insert into Skills (SkillID, SkillName, AlumniID) values (28, 'Creative Thinking', 21);
insert into Skills (SkillID, SkillName, AlumniID) values (29, 'Adaptability', 15);
insert into Skills (SkillID, SkillName, AlumniID) values (30, 'Attention to Detail', 28);
insert into Skills (SkillID, SkillName, AlumniID) values (31, 'Organization', 36);
insert into Skills (SkillID, SkillName, AlumniID) values (32, 'Interpersonal Skills', 6);
insert into Skills (SkillID, SkillName, AlumniID) values (33, 'Conflict Resolution', 28);
insert into Skills (SkillID, SkillName, AlumniID) values (34, 'Decision Making', 6);
insert into Skills (SkillID, SkillName, AlumniID) values (35, 'Technical Skills', 11);
insert into Skills (SkillID, SkillName, AlumniID) values (36, 'Analytical Skills', 37);
insert into Skills (SkillID, SkillName, AlumniID) values (37, 'Communication Skills', 14);
insert into Skills (SkillID, SkillName, AlumniID) values (38, 'Collaboration', 31);
insert into Skills (SkillID, SkillName, AlumniID) values (39, 'Self-Motivation', 14);
insert into Skills (SkillID, SkillName, AlumniID) values (40, 'Empathy', 10);


insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (1, 14, 29, 'Hey', '2024-04-21 05:51:08');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (2, 26, 29, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-07-01 23:07:42');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (3, 29, 22, 'Congratulations on landing your new job! I''m so happy for you!', '2024-05-13 11:37:24');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (4, 10, 7, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2023-12-11 05:20:50');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (5, 7, 13, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2023-12-19 01:17:16');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (6, 14, 5, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2024-05-29 08:33:10');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (7, 2, 33, 'Hey', '2023-12-16 23:44:43');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (8, 2, 6, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-10-13 14:32:48');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (9, 15, 2, 'Congratulations on landing your new job! I''m so happy for you!', '2024-03-08 05:23:59');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (10, 7, 23, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2023-12-26 13:54:38');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (11, 37, 19, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2024-07-17 18:32:24');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (12, 38, 1, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2024-02-20 18:49:51');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (13, 40, 5, 'Hey', '2024-06-02 14:17:58');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (14, 24, 37, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-04-16 02:41:21');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (15, 16, 25, 'Congratulations on landing your new job! I''m so happy for you!', '2024-11-16 21:35:19');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (16, 34, 30, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2024-11-12 04:04:23');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (17, 7, 3, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2024-05-04 11:21:03');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (18, 22, 20, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2024-07-07 00:16:52');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (19, 1, 21, 'Hey', '2024-11-13 19:32:57');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (20, 21, 29, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-08-30 09:58:21');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (21, 30, 13, 'Congratulations on landing your new job! I''m so happy for you!', '2024-07-29 07:36:54');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (22, 26, 38, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2024-05-16 20:57:53');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (23, 4, 36, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2023-12-22 16:50:20');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (24, 13, 34, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2024-02-24 14:39:10');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (25, 14, 32, 'Hey', '2024-09-26 08:28:20');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (26, 2, 38, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-08-13 08:37:55');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (27, 14, 5, 'Congratulations on landing your new job! I''m so happy for you!', '2024-08-27 09:47:29');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (28, 33, 2, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2024-03-10 00:01:19');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (29, 15, 39, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2024-04-01 22:28:03');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (30, 11, 22, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2023-12-08 09:05:03');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (31, 33, 3, 'Hey', '2024-08-03 19:44:37');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (32, 34, 25, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-09-10 09:51:31');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (33, 6, 20, 'Congratulations on landing your new job! I''m so happy for you!', '2024-07-30 17:51:48');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (34, 12, 3, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2024-10-15 23:26:08');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (35, 31, 27, 'I saw your LinkedIn update about your new job. That''s awesome news!', '2024-03-18 07:59:45');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (36, 24, 17, 'Have you considered freelancing? I know someone who could use your skills on a project.', '2024-06-07 13:23:08');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (37, 35, 33, 'Hey', '2024-11-13 09:01:09');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (38, 34, 27, 'I heard about a job opening at XYZ company that might be a good fit for you!', '2024-08-11 11:04:19');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (39, 37, 34, 'Congratulations on landing your new job! I''m so happy for you!', '2024-09-14 17:30:12');
insert into Messages (MessageID, SenderAlumniID, ReceiverAlumniID, MessageContent, TimeStamp) values (40, 31, 1, 'I have a contact at ABC company who is looking to hire. Let me know if you want me to connect you.', '2024-10-02 15:52:47');

insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (1, 8, 'Manager', 'Roombo', '2021-08-26', '2024-07-23', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (2, 27, 'Sales Associate', 'Wordtune', '2022-02-07', '2024-02-13', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (3, 2, 'Customer Service Representative', 'Realcube', '2022-10-26', '2024-04-27', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (4, 24, 'IT Specialist', 'Thoughtstorm', '2022-01-18', '2024-02-29', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (5, 33, 'Marketing Coordinator', 'Yacero', '2022-06-05', '2024-10-29', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (6, 36, 'Accountant', 'Babbleset', '2020-11-13', '2024-11-29', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (7, 16, 'Human Resources Manager', 'Kamba', '2023-07-24', '2024-10-05', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (8, 8, 'Operations Supervisor', 'Rhyloo', '2022-09-07', '2024-05-17', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (9, 3, 'Administrative Assistant', 'Flashdog', '2023-08-18', '2024-01-20', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (10, 5, 'Warehouse Worker', 'Jatri', '2021-05-21', '2024-10-02', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (11, 5, 'Manager', 'Topicblab', '2023-07-04', '2024-02-04', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (12, 11, 'Sales Associate', 'Jayo', '2022-02-14', '2024-03-24', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (13, 2, 'Customer Service Representative', 'Quatz', '2021-11-24', '2024-05-12', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (14, 1, 'IT Specialist', 'Yata', '2022-05-17', '2024-12-01', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (15, 14, 'Marketing Coordinator', 'Kayveo', '2023-05-06', '2024-03-25', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (16, 5, 'Accountant', 'Dabtype', '2021-01-29', '2024-05-10', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (17, 23, 'Human Resources Manager', 'Skimia', '2021-06-15', '2023-12-21', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (18, 11, 'Operations Supervisor', 'Flipstorm', '2020-01-07', '2024-06-01', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (19, 34, 'Administrative Assistant', 'Abatz', '2021-10-02', '2024-04-04', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (20, 23, 'Warehouse Worker', 'Dynabox', '2021-02-24', '2024-03-28', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (21, 16, 'Manager', 'Realmix', '2022-08-26', '2024-02-04', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (22, 6, 'Sales Associate', 'Yozio', '2022-06-22', '2024-05-12', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (23, 22, 'Customer Service Representative', 'Brainsphere', '2021-08-29', '2024-03-21', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (24, 38, 'IT Specialist', 'Gabspot', '2023-08-18', '2024-07-31', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (25, 32, 'Marketing Coordinator', 'Fivechat', '2022-05-29', '2024-05-18', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (26, 10, 'Accountant', 'Quaxo', '2021-07-14', '2024-05-23', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (27, 21, 'Human Resources Manager', 'Skynoodle', '2021-04-13', '2024-07-24', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (28, 11, 'Operations Supervisor', 'Aimbu', '2021-03-29', '2023-12-19', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (29, 39, 'Administrative Assistant', 'Oyoba', '2020-05-02', '2024-07-01', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (30, 30, 'Warehouse Worker', 'Miboo', '2022-03-24', '2024-01-20', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (31, 37, 'Manager', 'Browsedrive', '2020-09-05', '2024-04-15', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (32, 32, 'Sales Associate', 'Zoonder', '2023-10-11', '2024-07-27', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (33, 3, 'Customer Service Representative', 'Ozu', '2023-08-08', '2024-03-10', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (34, 27, 'IT Specialist', 'Dynava', '2020-05-27', '2024-10-05', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (35, 27, 'Marketing Coordinator', 'Realmix', '2022-06-01', '2024-05-23', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (36, 2, 'Accountant', 'Flipopia', '2022-11-02', '2024-03-12', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (37, 27, 'Human Resources Manager', 'Jaxspan', '2020-09-01', '2024-10-25', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (38, 11, 'Operations Supervisor', 'Mydeo', '2021-12-11', '2024-06-14', false);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (39, 15, 'Administrative Assistant', 'Photofeed', '2020-11-29', '2024-04-16', true);
insert into WorkExperience (ExperienceID, AlumniID, Role, Company, StartDate, EndDate, IsCurrent) values (40, 27, 'Warehouse Worker', 'Voonder', '2022-12-14', '2024-09-04', true);


insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (1, 18, 10, 'followed a user', '2023-12-08 23:45:49');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (2, 32, 30, 'liked a post', '2024-01-03 18:18:28');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (3, 38, 40, 'commented on a video', '2023-12-23 02:50:08');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (4, 5, 1, 'created a new post', '2024-01-08 13:31:29');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (5, 39, 5, 'sent a message', '2023-12-19 07:43:52');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (6, 27, 11, 'rated a product', '2023-12-17 00:13:50');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (7, 37, 39, 'liked a post', '2023-12-26 08:58:52');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (8, 28, 10, 'commented on a video', '2023-12-05 17:07:51');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (9, 30, 11, 'saved a link', '2023-12-13 14:41:33');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (10, 10, 23, 'rated a product', '2023-12-11 17:04:01');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (11, 29, 17, 'saved a link', '2023-12-15 14:31:30');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (12, 36, 24, 'updated profile picture', '2023-12-07 12:35:48');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (13, 19, 16, 'saved a link', '2023-12-17 23:56:14');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (14, 33, 28, 'sent a message', '2024-01-05 20:18:41');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (15, 30, 6, 'created a new post', '2023-12-12 19:37:44');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (16, 29, 10, 'updated profile picture', '2023-12-30 14:17:47');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (17, 13, 34, 'rated a product', '2023-12-29 07:52:23');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (18, 11, 4, 'followed a user', '2023-12-27 08:31:36');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (19, 7, 8, 'sent a message', '2024-01-09 14:45:13');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (20, 5, 38, 'logged in', '2023-12-18 03:25:20');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (21, 19, 23, 'logged in', '2024-01-09 18:33:25');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (22, 5, 7, 'logged in', '2023-12-25 23:50:00');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (23, 7, 38, 'followed a user', '2023-12-25 14:14:48');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (24, 39, 31, 'logged in', '2023-12-03 06:49:30');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (25, 26, 35, 'rated a product', '2023-12-06 18:20:24');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (26, 28, 1, 'sent a message', '2023-12-28 13:05:57');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (27, 9, 14, 'shared a photo', '2024-01-06 06:47:33');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (28, 38, 8, 'logged in', '2023-12-12 02:40:36');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (29, 4, 6, 'shared a photo', '2024-01-06 21:09:22');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (30, 15, 6, 'sent a message', '2023-12-24 16:59:48');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (31, 31, 29, 'logged in', '2024-01-04 20:46:59');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (32, 34, 1, 'liked a post', '2023-12-05 06:01:05');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (33, 17, 8, 'created a new post', '2024-01-05 12:40:51');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (34, 25, 21, 'logged in', '2024-01-04 22:11:01');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (35, 13, 39, 'updated profile picture', '2023-12-06 05:45:38');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (36, 4, 9, 'sent a message', '2023-12-31 16:00:02');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (37, 22, 4, 'logged in', '2023-12-23 19:46:41');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (38, 6, 19, 'liked a post', '2024-01-03 23:16:39');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (39, 3, 13, 'created a new post', '2023-12-14 17:10:54');
insert into Actions (ActionID, AlumniID, AdminID, ActionType, ActionTS) values (40, 11, 5, 'commented on a video', '2023-12-03 10:35:34');


insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (1, 28, 8, 'Engaging in illegal activities', '2023-12-18 22:41:05');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (2, 26, 7, 'Violating terms of service', '2023-12-09 01:58:34');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (3, 9, 29, 'Posting inappropriate content', '2023-12-07 00:24:04');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (4, 6, 26, 'Violating community guidelines', '2023-12-04 04:51:26');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (5, 19, 18, 'Spamming', '2023-12-22 20:59:15');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (6, 20, 11, 'Fraudulent activity', '2023-12-13 21:54:55');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (7, 23, 22, 'Inappropriate language', '2023-12-23 06:52:39');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (8, 13, 31, 'Inappropriate language', '2023-12-29 16:07:14');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (9, 2, 3, 'Posting inappropriate content', '2023-12-15 04:34:12');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (10, 28, 8, 'Inappropriate language', '2023-12-15 04:35:04');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (11, 15, 2, 'Posting inappropriate content', '2024-01-05 05:23:00');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (12, 9, 12, 'Inappropriate language', '2023-12-30 13:00:38');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (13, 27, 23, 'Spamming', '2023-12-21 02:44:09');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (14, 19, 28, 'Sharing personal information', '2023-12-06 09:56:40');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (15, 33, 3, 'Inappropriate language', '2024-01-05 07:39:19');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (16, 17, 35, 'Sharing personal information', '2023-12-11 08:27:06');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (17, 32, 38, 'Spamming', '2023-12-07 03:52:38');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (18, 4, 9, 'Fraudulent activity', '2023-12-13 01:04:06');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (19, 5, 11, 'Inappropriate language', '2023-12-12 09:02:12');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (20, 31, 9, 'Inappropriate language', '2023-12-08 05:51:44');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (21, 23, 5, 'Inappropriate language', '2023-12-04 10:06:53');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (22, 11, 11, 'Spamming', '2023-12-11 13:40:28');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (23, 31, 30, 'Spamming', '2023-12-09 04:25:03');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (24, 29, 7, 'Fraudulent activity', '2023-12-25 16:27:05');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (25, 21, 27, 'Spamming', '2023-12-22 23:30:08');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (26, 10, 2, 'Inappropriate language', '2023-12-19 16:36:42');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (27, 32, 11, 'Violating community guidelines', '2023-12-23 16:48:12');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (28, 10, 26, 'Violating terms of service', '2024-01-01 02:44:25');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (29, 3, 33, 'Impersonation', '2023-12-05 08:06:23');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (30, 31, 12, 'Sharing personal information', '2023-12-22 16:41:19');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (31, 29, 36, 'Sharing personal information', '2023-12-24 19:28:53');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (32, 18, 38, 'Sharing personal information', '2023-12-12 12:43:19');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (33, 31, 8, 'Fraudulent activity', '2023-12-30 13:30:40');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (34, 6, 14, 'Harassment', '2023-12-29 02:23:44');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (35, 21, 2, 'Spamming', '2023-12-08 06:56:48');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (36, 21, 31, 'Violating terms of service', '2024-01-03 13:04:08');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (37, 37, 31, 'Violating terms of service', '2024-01-05 17:43:09');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (38, 26, 12, 'Violating community guidelines', '2023-12-14 01:13:46');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (39, 16, 12, 'Fraudulent activity', '2023-12-23 12:45:29');
insert into Warnings (WarningID, AlumniID, AdminID, Reason, TimeStamp) values (40, 16, 8, 'Engaging in illegal activities', '2023-12-30 15:41:13');


insert into Administrator (AdminID, Name, Email, Role) values (1, 'Julietta Maskelyne', 'jmaskelyne0@adobe.com', 'Super Admin');
insert into Administrator (AdminID, Name, Email, Role) values (2, 'Amelia Jon', 'ajon1@cnet.com', 'Moderator');
insert into Administrator (AdminID, Name, Email, Role) values (3, 'Rodolph Billin', 'rbillin2@plala.or.jp', 'Moderator');
insert into Administrator (AdminID, Name, Email, Role) values (4, 'Nanny Swett', 'nswett3@miibeian.gov.cn', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (5, 'Daveta Lowdwell', 'dlowdwell4@yahoo.co.jp', 'Super Admin');
insert into Administrator (AdminID, Name, Email, Role) values (6, 'Alexandrina Dart', 'adart5@goo.ne.jp', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (7, 'Harriett Drew-Clifton', 'hdrewclifton6@cbc.ca', 'Admin');
insert into Administrator (AdminID, Name, Email, Role) values (8, 'Dorotea Colecrough', 'dcolecrough7@alexa.com', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (9, 'Karlotte Mora', 'kmora8@e-recht24.de', 'Consultant');
insert into Administrator (AdminID, Name, Email, Role) values (10, 'Miquela Emmet', 'memmet9@loc.gov', 'Manager');
insert into Administrator (AdminID, Name, Email, Role) values (11, 'Eziechiele Ellery', 'eellerya@reddit.com', 'Admin');
insert into Administrator (AdminID, Name, Email, Role) values (12, 'Con Hennington', 'chenningtonb@networksolutions.com', 'Support');
insert into Administrator (AdminID, Name, Email, Role) values (13, 'Judon Satchell', 'jsatchellc@nature.com', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (14, 'Marc Oseman', 'mosemand@cdc.gov', 'Super Admin');
insert into Administrator (AdminID, Name, Email, Role) values (15, 'Lovell MacGown', 'lmacgowne@boston.com', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (16, 'Nico Hoyle', 'nhoylef@youku.com', 'Tester');
insert into Administrator (AdminID, Name, Email, Role) values (17, 'Silvio Riolfi', 'sriolfig@acquirethisname.com', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (18, 'De Yurchishin', 'dyurchishinh@geocities.com', 'Consultant');
insert into Administrator (AdminID, Name, Email, Role) values (19, 'Davy Toe', 'dtoei@liveinternet.ru', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (20, 'Karlotte Braisby', 'kbraisbyj@uiuc.edu', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (21, 'Trev Edrich', 'tedrichk@howstuffworks.com', 'Super Admin');
insert into Administrator (AdminID, Name, Email, Role) values (22, 'Milty Paynton', 'mpayntonl@sakura.ne.jp', 'Developer');
insert into Administrator (AdminID, Name, Email, Role) values (23, 'Ferdie Elloit', 'felloitm@hatena.ne.jp', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (24, 'Nora Blint', 'nblintn@g.co', 'Developer');
insert into Administrator (AdminID, Name, Email, Role) values (25, 'Nichole Softley', 'nsoftleyo@people.com.cn', 'Admin');
insert into Administrator (AdminID, Name, Email, Role) values (26, 'Guthrie Sommerly', 'gsommerlyp@japanpost.jp', 'Super Admin');
insert into Administrator (AdminID, Name, Email, Role) values (27, 'Anabelle Afonso', 'aafonsoq@bizjournals.com', 'Tester');
insert into Administrator (AdminID, Name, Email, Role) values (28, 'Elayne Aucutt', 'eaucuttr@lycos.com', 'Support');
insert into Administrator (AdminID, Name, Email, Role) values (29, 'Donella Crowther', 'dcrowthers@i2i.jp', 'Support');
insert into Administrator (AdminID, Name, Email, Role) values (30, 'Kingsly Dunphy', 'kdunphyt@bbb.org', 'Developer');
insert into Administrator (AdminID, Name, Email, Role) values (31, 'Collie Brookes', 'cbrookesu@rediff.com', 'Consultant');
insert into Administrator (AdminID, Name, Email, Role) values (32, 'Maura Tanfield', 'mtanfieldv@timesonline.co.uk', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (33, 'Virgil Maevela', 'vmaevelaw@constantcontact.com', 'Coordinator');
insert into Administrator (AdminID, Name, Email, Role) values (34, 'Carmine Crunden', 'ccrundenx@plala.or.jp', 'Moderator');
insert into Administrator (AdminID, Name, Email, Role) values (35, 'Sherwood Liversage', 'sliversagey@weebly.com', 'Admin');
insert into Administrator (AdminID, Name, Email, Role) values (36, 'Kassandra Alejandro', 'kalejandroz@go.com', 'Admin');
insert into Administrator (AdminID, Name, Email, Role) values (37, 'Shane Erdes', 'serdes10@last.fm', 'Analyst');
insert into Administrator (AdminID, Name, Email, Role) values (38, 'Thurstan Spurman', 'tspurman11@taobao.com', 'Consultant');
insert into Administrator (AdminID, Name, Email, Role) values (39, 'Ranee Covolini', 'rcovolini12@independent.co.uk', 'Tester');
insert into Administrator (AdminID, Name, Email, Role) values (40, 'Alwyn Belson', 'abelson13@cargocollective.com', 'Tester');


insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (1, 'Mariquilla Faull', 'Manager', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/SdlypcY.png', 'Volunteered at a local animal shelter for 3 months', 1999);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (2, 'Rosamond Wilcinskis', 'Sales Associate', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/SdlypcY.png', 'Part-time job as a tutor for high school students', 2004);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (3, 'Andy Haggett', 'Customer Service Representative', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 1998);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (4, 'Lexi Oiseau', 'IT Specialist', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 1993);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (5, 'Ferrell Skottle', 'Marketing Coordinator', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 2009);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (6, 'Erma Chamberlain', 'Accountant', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/p37Is1i.png', 'Volunteered at a local animal shelter for 3 months', 1997);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (7, 'Carlita Cranke', 'Human Resources Manager', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/SdlypcY.png', 'Part-time job as a tutor for high school students', 2009);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (8, 'Bella Blissett', 'Operations Supervisor', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/u49LBXk.png', 'Part-time job as a tutor for high school students', 1994);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (9, 'Alisander Hoys', 'Administrative Assistant', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/p37Is1i.png', 'Volunteered at a local animal shelter for 3 months', 2002);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (10, 'Andres Lambertz', 'Warehouse Worker', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/p37Is1i.png', 'Interned at a tech startup for 6 months', 2012);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (11, 'Garland Benneyworth', 'Manager', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/p37Is1i.png', 'Completed a summer internship at a marketing agency', 1996);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (12, 'Kellsie Meadmore', 'Sales Associate', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 2001);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (13, 'Jarad Wilmut', 'Customer Service Representative', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/SdlypcY.png', 'Interned at a tech startup for 6 months', 2012);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (14, 'Ellwood Lightning', 'IT Specialist', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/p37Is1i.png', 'Completed a summer internship at a marketing agency', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (15, 'Rafaellle Martijn', 'Marketing Coordinator', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 2003);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (16, 'Rodina Gladwish', 'Accountant', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 2004);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (17, 'Gwendolen Perfili', 'Human Resources Manager', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/u49LBXk.png', 'Interned at a tech startup for 6 months', 2007);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (18, 'Roz Blakden', 'Operations Supervisor', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/p37Is1i.png', 'Volunteered at a local animal shelter for 3 months', 2003);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (19, 'Dotty Chessil', 'Administrative Assistant', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/SdlypcY.png', 'Completed a summer internship at a marketing agency', 2002);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (20, 'Thoma Gainsborough', 'Warehouse Worker', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 2009);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (21, 'Jessee Glenfield', 'Manager', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (22, 'Tresa Voelker', 'Sales Associate', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/SdlypcY.png', 'Part-time job as a tutor for high school students', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (23, 'Bibi Hundey', 'Customer Service Representative', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 1999);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (24, 'Kris Picot', 'IT Specialist', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/p37Is1i.png', 'Worked as a barista for 1 year', 2006);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (25, 'Lay Chaudhry', 'Marketing Coordinator', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/p37Is1i.png', 'Worked as a barista for 1 year', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (26, 'Griffy Becken', 'Accountant', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/SdlypcY.png', 'Volunteered at a local animal shelter for 3 months', 1995);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (27, 'Osgood Calvie', 'Human Resources Manager', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/u49LBXk.png', 'Interned at a tech startup for 6 months', 2005);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (28, 'Inessa Gennrich', 'Operations Supervisor', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/SdlypcY.png', 'Worked as a barista for 1 year', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (29, 'Biddy Knock', 'Administrative Assistant', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/u49LBXk.png', 'Volunteered at a local animal shelter for 3 months', 1994);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (30, 'Francois Pinkett', 'Warehouse Worker', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/u49LBXk.png', 'Worked as a barista for 1 year', 2006);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (31, 'Hettie Wort', 'Manager', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 1998);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (32, 'Sashenka Hovell', 'Sales Associate', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/SdlypcY.png', 'Completed a summer internship at a marketing agency', 2003);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (33, 'Sada Imms', 'Customer Service Representative', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/SdlypcY.png', 'Volunteered at a local animal shelter for 3 months', 2009);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (34, 'Clarence Goning', 'IT Specialist', 'Recent graduate eager to start a career in finance', 'https://i.imgur.com/SdlypcY.png', 'Interned at a tech startup for 6 months', 2011);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (35, 'Hadlee Fatscher', 'Marketing Coordinator', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/SdlypcY.png', 'Completed a summer internship at a marketing agency', 1997);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (36, 'Sonnie Shipston', 'Accountant', 'Creative problem-solver with a knack for project management', 'https://i.imgur.com/p37Is1i.png', 'Volunteered at a local animal shelter for 3 months', 1992);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (37, 'Binnie Burfitt', 'Human Resources Manager', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/u49LBXk.png', 'Part-time job as a tutor for high school students', 1992);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (38, 'Wat Slader', 'Operations Supervisor', 'Passionate individual with a strong background in marketing', 'https://i.imgur.com/p37Is1i.png', 'Interned at a tech startup for 6 months', 2008);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (39, 'Rudd Phorsby', 'Administrative Assistant', 'Experienced professional seeking new opportunities in the tech industry', 'https://i.imgur.com/p37Is1i.png', 'Worked as a barista for 1 year', 1995);
insert into Alumni (AlumniID, Name, Major, AboutMe, ProfilePic, WorkExperience, GradYear) values (40, 'Latisha Dewi', 'Warehouse Worker', 'Detail-oriented team player with a background in customer service', 'https://i.imgur.com/p37Is1i.png', 'Part-time job as a tutor for high school students', 2002);


insert into Candidate_Traits (CandidateID, TraitID) values (7, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (4, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (11, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (15, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (2, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (39, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (17, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (5, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (38, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (37, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (18, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (37, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (26, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (4, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (21, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (26, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (8, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (24, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (40, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (4, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (3, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (29, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (33, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (26, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (22, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (19, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (22, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (28, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (30, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (21, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (20, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (40, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (37, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (22, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (29, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (1, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (18, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (34, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (11, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (9, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (32, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (23, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (13, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (18, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (33, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (40, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (39, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (9, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (38, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (30, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (16, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (36, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (12, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (2, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (1, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (17, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (12, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (6, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (3, 3);
insert into Candidate_Traits (CandidateID, TraitID) values (20, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (16, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (23, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (23, 6);
insert into Candidate_Traits (CandidateID, TraitID) values (31, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (4, 4);
insert into Candidate_Traits (CandidateID, TraitID) values (27, 5);
insert into Candidate_Traits (CandidateID, TraitID) values (26, 1);
insert into Candidate_Traits (CandidateID, TraitID) values (8, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (38, 2);
insert into Candidate_Traits (CandidateID, TraitID) values (23, 2);


insert into Alumni_Skills (AlumniID, SkillsID) values (6, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (17, 28);
insert into Alumni_Skills (AlumniID, SkillsID) values (15, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (22, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (5, 38);
insert into Alumni_Skills (AlumniID, SkillsID) values (5, 32);
insert into Alumni_Skills (AlumniID, SkillsID) values (27, 28);
insert into Alumni_Skills (AlumniID, SkillsID) values (15, 2);
insert into Alumni_Skills (AlumniID, SkillsID) values (27, 22);
insert into Alumni_Skills (AlumniID, SkillsID) values (27, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (25, 34);
insert into Alumni_Skills (AlumniID, SkillsID) values (14, 26);
insert into Alumni_Skills (AlumniID, SkillsID) values (24, 2);
insert into Alumni_Skills (AlumniID, SkillsID) values (35, 8);
insert into Alumni_Skills (AlumniID, SkillsID) values (39, 13);
insert into Alumni_Skills (AlumniID, SkillsID) values (38, 30);
insert into Alumni_Skills (AlumniID, SkillsID) values (12, 9);
insert into Alumni_Skills (AlumniID, SkillsID) values (3, 19);
insert into Alumni_Skills (AlumniID, SkillsID) values (1, 2);
insert into Alumni_Skills (AlumniID, SkillsID) values (25, 20);
insert into Alumni_Skills (AlumniID, SkillsID) values (21, 15);
insert into Alumni_Skills (AlumniID, SkillsID) values (2, 2);
insert into Alumni_Skills (AlumniID, SkillsID) values (16, 32);
insert into Alumni_Skills (AlumniID, SkillsID) values (19, 1);
insert into Alumni_Skills (AlumniID, SkillsID) values (11, 10);
insert into Alumni_Skills (AlumniID, SkillsID) values (23, 30);
insert into Alumni_Skills (AlumniID, SkillsID) values (29, 19);
insert into Alumni_Skills (AlumniID, SkillsID) values (3, 3);
insert into Alumni_Skills (AlumniID, SkillsID) values (20, 39);
insert into Alumni_Skills (AlumniID, SkillsID) values (40, 32);
insert into Alumni_Skills (AlumniID, SkillsID) values (37, 8);
insert into Alumni_Skills (AlumniID, SkillsID) values (23, 12);
insert into Alumni_Skills (AlumniID, SkillsID) values (36, 19);
insert into Alumni_Skills (AlumniID, SkillsID) values (3, 23);
insert into Alumni_Skills (AlumniID, SkillsID) values (30, 35);
insert into Alumni_Skills (AlumniID, SkillsID) values (5, 34);
insert into Alumni_Skills (AlumniID, SkillsID) values (21, 6);
insert into Alumni_Skills (AlumniID, SkillsID) values (1, 7);
insert into Alumni_Skills (AlumniID, SkillsID) values (23, 31);
insert into Alumni_Skills (AlumniID, SkillsID) values (19, 22);
insert into Alumni_Skills (AlumniID, SkillsID) values (15, 16);
insert into Alumni_Skills (AlumniID, SkillsID) values (10, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (39, 6);
insert into Alumni_Skills (AlumniID, SkillsID) values (39, 10);
insert into Alumni_Skills (AlumniID, SkillsID) values (2, 38);
insert into Alumni_Skills (AlumniID, SkillsID) values (4, 3);
insert into Alumni_Skills (AlumniID, SkillsID) values (26, 40);
insert into Alumni_Skills (AlumniID, SkillsID) values (37, 12);
insert into Alumni_Skills (AlumniID, SkillsID) values (27, 36);
insert into Alumni_Skills (AlumniID, SkillsID) values (31, 19);
insert into Alumni_Skills (AlumniID, SkillsID) values (1, 36);
insert into Alumni_Skills (AlumniID, SkillsID) values (36, 36);
insert into Alumni_Skills (AlumniID, SkillsID) values (5, 7);
insert into Alumni_Skills (AlumniID, SkillsID) values (36, 37);
insert into Alumni_Skills (AlumniID, SkillsID) values (25, 27);
insert into Alumni_Skills (AlumniID, SkillsID) values (37, 7);
insert into Alumni_Skills (AlumniID, SkillsID) values (16, 3);
insert into Alumni_Skills (AlumniID, SkillsID) values (14, 20);
insert into Alumni_Skills (AlumniID, SkillsID) values (3, 10);
insert into Alumni_Skills (AlumniID, SkillsID) values (26, 4);
insert into Alumni_Skills (AlumniID, SkillsID) values (30, 39);
insert into Alumni_Skills (AlumniID, SkillsID) values (8, 32);
insert into Alumni_Skills (AlumniID, SkillsID) values (23, 15);
insert into Alumni_Skills (AlumniID, SkillsID) values (13, 4);
insert into Alumni_Skills (AlumniID, SkillsID) values (12, 14);
insert into Alumni_Skills (AlumniID, SkillsID) values (29, 13);
insert into Alumni_Skills (AlumniID, SkillsID) values (27, 6);
insert into Alumni_Skills (AlumniID, SkillsID) values (20, 35);
insert into Alumni_Skills (AlumniID, SkillsID) values (40, 2);
insert into Alumni_Skills (AlumniID, SkillsID) values (5, 24);
insert into Alumni_Skills (AlumniID, SkillsID) values (28, 35);
insert into Alumni_Skills (AlumniID, SkillsID) values (3, 39);
insert into Alumni_Skills (AlumniID, SkillsID) values (38, 16);
insert into Alumni_Skills (AlumniID, SkillsID) values (25, 7);
insert into Alumni_Skills (AlumniID, SkillsID) values (23, 40);
insert into Alumni_Skills (AlumniID, SkillsID) values (18, 11);
insert into Alumni_Skills (AlumniID, SkillsID) values (13, 3);
insert into Alumni_Skills (AlumniID, SkillsID) values (17, 19);
insert into Alumni_Skills (AlumniID, SkillsID) values (18, 14);
insert into Alumni_Skills (AlumniID, SkillsID) values (30, 4);
insert into Alumni_Skills (AlumniID, SkillsID) values (31, 30);
insert into Alumni_Skills (AlumniID, SkillsID) values (39, 26);
insert into Alumni_Skills (AlumniID, SkillsID) values (4, 26);
insert into Alumni_Skills (AlumniID, SkillsID) values (1, 12);
insert into Alumni_Skills (AlumniID, SkillsID) values (21, 24);
insert into Alumni_Skills (AlumniID, SkillsID) values (25, 30);
insert into Alumni_Skills (AlumniID, SkillsID) values (7, 28);
insert into Alumni_Skills (AlumniID, SkillsID) values (22, 23);
insert into Alumni_Skills (AlumniID, SkillsID) values (32, 28);
insert into Alumni_Skills (AlumniID, SkillsID) values (40, 24);
insert into Alumni_Skills (AlumniID, SkillsID) values (24, 15);
insert into Alumni_Skills (AlumniID, SkillsID) values (35, 4);
insert into Alumni_Skills (AlumniID, SkillsID) values (8, 6);
insert into Alumni_Skills (AlumniID, SkillsID) values (34, 37);



