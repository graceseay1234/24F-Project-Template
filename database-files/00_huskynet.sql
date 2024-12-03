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
  Uptime TIME,
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
  RecieverAlumniID INT,
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
  ActionTS VARCHAR(50),
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
  ProfilePic VARBINARY(10000),
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





