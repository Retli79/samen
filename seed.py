from db.models import User, Post, FriendRequest, Group, GroupMembership, GroupRequest, DbComment
from db.database import SessionLocal
from datetime import datetime

def seed():
    db = SessionLocal()

    # Create users
    users = [
        User(username='john', email='john@example.com', password='123'),
        User(username='jane', email='jane@example.com', password='123'),
        User(username='alice', email='alice@example.com', password='123'),
        User(username='bob', email='bob@example.com', password='123'),
        User(username='charlie', email='charlie@example.com', password='123'),
        User(username='david', email='david@example.com', password='123'),
        User(username='eve', email='eve@example.com', password='123'),
        User(username='frank', email='frank@example.com', password='123'),
        User(username='grace', email='grace@example.com', password='123'),
        User(username='hank', email='hank@example.com', password='123')
    ]
    
    db.add_all(users)
    db.commit()

    # Create posts
    posts = [
        Post(image_url='http://example.com/pic1.jpg', image_url_type='absolute', caption='First picture', title='First Post', content='This is the first post content', owner_id=1),
        Post(image_url='http://example.com/pic2.jpg', image_url_type='absolute', caption='Second picture', title='Second Post', content='This is the second post content', owner_id=2),
        Post(image_url='http://example.com/pic3.jpg', image_url_type='absolute', caption='Third picture', title='Third Post', content='This is the third post content', owner_id=3),
        Post(image_url='http://example.com/pic4.jpg', image_url_type='absolute', caption='Fourth picture', title='Fourth Post', content='This is the fourth post content', owner_id=4),
        Post(image_url='http://example.com/pic5.jpg', image_url_type='absolute', caption='Fifth picture', title='Fifth Post', content='This is the fifth post content', owner_id=5),
        Post(image_url='http://example.com/pic6.jpg', image_url_type='absolute', caption='Sixth picture', title='Sixth Post', content='This is the sixth post content', owner_id=6),
        Post(image_url='http://example.com/pic7.jpg', image_url_type='absolute', caption='Seventh picture', title='Seventh Post', content='This is the seventh post content', owner_id=7),
        Post(image_url='http://example.com/pic8.jpg', image_url_type='absolute', caption='Eighth picture', title='Eighth Post', content='This is the eighth post content', owner_id=8),
        Post(image_url='http://example.com/pic9.jpg', image_url_type='absolute', caption='Ninth picture', title='Ninth Post', content='This is the ninth post content', owner_id=9),
        Post(image_url='http://example.com/pic10.jpg', image_url_type='absolute', caption='Tenth picture', title='Tenth Post', content='This is the tenth post content', owner_id=10)
    ]
    
    db.add_all(posts)
    db.commit()

    # Create comments
    comments = [
        DbComment(text='Great post!', username='jane', timestamp=datetime.now(), post_id=1),
        DbComment(text='Nice post!', username='alice', timestamp=datetime.now(), post_id=2),
        DbComment(text='Interesting post!', username='bob', timestamp=datetime.now(), post_id=3),
        DbComment(text='Informative post!', username='charlie', timestamp=datetime.now(), post_id=4),
        DbComment(text='Awesome post!', username='david', timestamp=datetime.now(), post_id=5),
        DbComment(text='Fantastic post!', username='eve', timestamp=datetime.now(), post_id=6),
        DbComment(text='Excellent post!', username='frank', timestamp=datetime.now(), post_id=7),
        DbComment(text='Very good post!', username='grace', timestamp=datetime.now(), post_id=8),
        DbComment(text='Cool post!', username='hank', timestamp=datetime.now(), post_id=9),
        DbComment(text='Superb post!', username='john', timestamp=datetime.now(), post_id=10)
    ]
    
    db.add_all(comments)
    db.commit()

    # Create friend requests
    friend_requests = [
        FriendRequest(sender_id=1, receiver_id=2, status='accepted'),
        FriendRequest(sender_id=3, receiver_id=4, status='accepted'),
        FriendRequest(sender_id=5, receiver_id=6, status='accepted'),
        FriendRequest(sender_id=7, receiver_id=8, status='accepted'),
        FriendRequest(sender_id=9, receiver_id=10, status='accepted')
    ]
    
    db.add_all(friend_requests)
    db.commit()

    # Create groups
    groups = [
        Group(name='Group 1', description='This is group 1', admin_id=1),
        Group(name='Group 2', description='This is group 2', admin_id=2)
    ]
    
    db.add_all(groups)
    db.commit()

    # Create group memberships
    group_memberships = [
        GroupMembership(user_id=1, group_id=1, role='admin'),
        GroupMembership(user_id=2, group_id=1, role='member'),
        GroupMembership(user_id=3, group_id=1, role='member'),
        GroupMembership(user_id=4, group_id=1, role='member'),
        GroupMembership(user_id=5, group_id=2, role='admin'),
        GroupMembership(user_id=6, group_id=2, role='member'),
        GroupMembership(user_id=7, group_id=2, role='member'),
        GroupMembership(user_id=8, group_id=2, role='member')
    ]
    
    db.add_all(group_memberships)
    db.commit()

    # Create group requests
    group_requests = [
        GroupRequest(sender_id=9, receiver_id=10, group_id=1, status='pending'),
        GroupRequest(sender_id=10, receiver_id=9, group_id=2, status='pending')
    ]
    
    db.add_all(group_requests)
    db.commit()

    db.close()

if __name__ == "__main__":
    seed()
