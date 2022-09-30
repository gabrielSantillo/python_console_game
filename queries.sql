insert into move(name, lower_damage_range, upper_damage_range)
values ('fire', 5, 10), ('water', 4, 8), ('grass', 3, 6), ('earth', 4, 8), ('electric', 4, 8), ('fly', 3, 6), ('dive', 2, 4), ('dig', 3, 6), ('surf', 4, 8),
('cut', 2, 4);

insert into computer_fighter (move_one, move_two, move_three, move_four, name, health) 
values (1, 5, 6, 10, 'Computer Fighter One', 20);

insert into client (username, password, joined_on) values ('gabriel', '123', now());

call select_user('gabriel', '123');

call add_fighter (4, 2, 5, 10, 7, 'fighter one');

call get_fighter_by_id(4);

call get_all_moves();

call add_fighter_points(50, 1);

call get_computer_fighter();

call get_user_fighter_by_fighter_id(1);

call get_user_fighter_by_fighter_id(1);

call get_all_moves_by_id(1);

call update_computer_life(10);

call get_computer_fighter();