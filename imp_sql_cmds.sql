-- Left Join
-- select * from posts left join users on posts.owner_id = users.id;
select posts.id as post_id, title as post_title, content as post_content, owner_id, email as owner_email
from posts
         left join users on posts.owner_id = users.id;

-- Right Join
select *
from posts
         right join users on posts.owner_id = users.id;

-- Group By
select users.id
from posts
         left join users on posts.owner_id = users.id
group by users.id;

-- Count -> Number of posts of each user -> Users with null post are ignored
select users.id, count(*)
from posts
         left join users on posts.owner_id = users.id
group by users.id;

-- Count -> Number of posts of each user -> Users with null post have count value of 1
select users.id, email, count(*)
from posts
         right join users on posts.owner_id = users.id
group by users.id;

-- Posts And Owner Information
select *
from posts
         right join users on posts.owner_id = users.id;

-- Count -> Number of posts of each user
select users.id, email, count(posts.id) as number_of_posts
from posts
         right join users on posts.owner_id = users.id
group by users.id;

-- Data Of Votes Table
Select *
from votes;

-- Data Of Posts Table
select *
from posts;

-- Number of votes on each posts
select posts.*, count(votes.user_id) as number_of_votes
from posts
         left join votes on posts.id = votes.post_id
group by posts.id;

-- Number of votes on a specific post
select id, title, content, owner_id, count(votes.post_id) as number_of_votes
from posts
         left join votes on posts.id = votes.post_id where posts.id = 12
group by posts.id;