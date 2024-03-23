from octosessionviewer import OctoSessionViewer


def main():
    import argparse
    parser = argparse.ArgumentParser(description='OctoSessionViewer')
    parser.add_argument('session_file', help='Path to the session file')
    parser.add_argument('--key', help='Key to decrypt the session file')
    parser.add_argument('--export', choices=['json', 'toml', 'str'], default='str', help='Export the session to the specified format')
    parser.add_argument('--extract', action='store_true', help='Extract the contents of the work directory')
    parser.add_argument('--extract-dir', default='./workdir', help='Directory to extract the work files to.')
    args = parser.parse_args()
    session = OctoSessionViewer.from_file(args.session_file, args.key)
    
    if args.export == 'str':
        print(session)
    
    elif args.export == 'json':
        print(session.to_json())
    
    elif args.export == 'toml':
        print(session.to_toml())

    if args.extract is True:
        session.extract_workdir(args.extract_dir)


if __name__ == '__main__':
    main()