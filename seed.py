from db.models import User, Post, FriendRequest, Group, GroupMembership, GroupRequest, DbComment,friends_table
from db.database import SessionLocal
from datetime import datetime
from db.hash import Hash

def seed():
    db = SessionLocal()

    # Create users
    password = '123'
    users = [
        User(username='john', email='john@example.com', password= Hash.bcrypt(password)),
        User(username='jane', email='jane@example.com', password=Hash.bcrypt(password)),
        User(username='alice', email='alice@example.com', password=Hash.bcrypt(password)),
        User(username='bob', email='bob@example.com', password=Hash.bcrypt(password)),
        User(username='charlie', email='charlie@example.com', password=Hash.bcrypt(password)),
        User(username='david', email='david@example.com', password=Hash.bcrypt(password)),
        User(username='eve', email='eve@example.com', password=Hash.bcrypt(password)),
        User(username='frank', email='frank@example.com', password=Hash.bcrypt(password)),
        User(username='grace', email='grace@example.com', password=Hash.bcrypt(password)),
        User(username='hank', email='hank@example.com', password=Hash.bcrypt(password))
    ]
    
    db.add_all(users)
    db.commit()

    # Create posts
    posts = [
        Post(image_url='https://cdn.pixabay.com/photo/2016/12/05/11/39/fox-1883658_640.jpg', image_url_type='absolute', caption='First picture', title='First Post', content='This is the first post content', owner_id=1),
        Post(image_url='https://i.natgeofe.com/k/c02b35d2-bfd7-4ed9-aad4-8e25627cd481/komodo-dragon-head-on_4x3.jpg', image_url_type='absolute', caption='Second picture', title='Second Post', content='This is the second post content', owner_id=2),
        Post(image_url='https://images.pexels.com/photos/45853/grey-crowned-crane-bird-crane-animal-45853.jpeg?cs=srgb&dl=pexels-pixabay-45853.jpg&fm=jpg', image_url_type='absolute', caption='Third picture', title='Third Post', content='This is the third post content', owner_id=3),
        Post(image_url='https://images.pexels.com/photos/1108099/pexels-photo-1108099.jpegg&fm=jpg', image_url_type='absolute', caption='Fourth picture', title='Fourth Post', content='This is the fourth post content', owner_id=4),
        Post(image_url='https://i.pinimg.com/originals/a6/94/c2/a694c2f6dac7497974c391c7ecb0e337.jpg', image_url_type='absolute', caption='Fifth picture', title='Fifth Post', content='This is the fifth post content', owner_id=5),
        Post(image_url='https://t3.ftcdn.net/jpg/07/37/16/14/360_F_737161452_oOt3F4JnOq2YzUqCX2NgKul7sfFrpqAp.jpg', image_url_type='absolute', caption='Sixth picture', title='Sixth Post', content='This is the sixth post content', owner_id=6),
        Post(image_url='https://wallpapers.com/images/featured/cute-animal-pictures-tscmynv1q1lo33f7.jpg', image_url_type='absolute', caption='Seventh picture', title='Seventh Post', content='This is the seventh post content', owner_id=7),
        Post(image_url='https://media.glamour.com/photos/56964cd993ef4b095210515b/16:9/w_1280,c_limit/fashion-2015-10-cute-baby-turtles-main.jpg', image_url_type='absolute', caption='Eighth picture', title='Eighth Post', content='This is the eighth post content', owner_id=8),
        Post(image_url='https://compote.slate.com/images/73f0857e-2a1a-4fea-b97a-bd4c241c01f5.jpg', image_url_type='absolute', caption='Ninth picture', title='Ninth Post', content='This is the ninth post content', owner_id=9),
        Post(image_url='https://ichef.bbci.co.uk/images/ic/1040x1040/p03t268b.jpg', image_url_type='absolute', caption='Tenth picture', title='Tenth Post', content='This is the tenth post content', owner_id=10)
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

    # Add friends
    friends_data = [
        (1, 2),  # john and jane are friends
        (3, 4),  # alice and bob are friends
        (5, 6),  # charlie and david are friends
        (7, 8),  # eve and frank are friends
        (9, 10)  # grace and hank are friends
    ]

    for friend_pair in friends_data:
        user1_id, user2_id = friend_pair
        db.execute(friends_table.insert().values(user_id=user1_id, friend_id=user2_id))
        db.execute(friends_table.insert().values(user_id=user2_id, friend_id=user1_id))

    db.commit()


    try:
        db.add_all(users)
        db.commit()
    except Exception as e:
        print(f"Error committing users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
