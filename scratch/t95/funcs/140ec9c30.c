char __fastcall sub_140EC9C30(__int64 a1)
{
  int v1; // eax
  __int64 v2; // rcx
  char result; // al
  char v4; // kr00_1

  v1 = *(_DWORD *)(a1 + 12);
  if ( v1 > 102427 )
  {
    if ( v1 <= 136406 )
    {
      if ( v1 <= 130285 )
      {
        if ( v1 <= 129644 )
        {
          if ( v1 != 102428 && v1 != 129559 )
            return 6;
          return 5;
        }
        if ( v1 != 129645 && v1 != 129650 )
          return 6;
      }
      else if ( v1 <= 131286 )
      {
        if ( v1 == 130286 )
          return 2;
        if ( v1 != 130486 )
          return 6;
      }
      else if ( v1 != 131287 )
      {
        if ( v1 != 132321 )
        {
          if ( v1 == 135973 )
            return 3;
          return 6;
        }
        return 5;
      }
    }
    else if ( v1 > 5260947 )
    {
      if ( v1 > 5512769 )
      {
        if ( v1 != 5512770 && v1 != 7520391 && v1 != 7580000 )
          return 6;
        return 5;
      }
      if ( v1 != 5260948 && v1 != 5314301 )
        return 6;
    }
    else if ( v1 <= 137888 )
    {
      if ( v1 == 136407 )
        return 5;
      if ( v1 != 136543 )
        return 6;
    }
    else if ( v1 != 137889 )
    {
      if ( v1 != 1300398 && v1 != 5250792 )
        return 6;
      return 5;
    }
    return 4;
  }
  v2 = (unsigned int)(v1 - 1);
  v4 = v1;
  result = 1;
  switch ( v2 )
  {
    case 0LL:
    case 11LL:
    case 28LL:
    case 59LL:
      return 2;
    case 1LL:
    case 2LL:
    case 3LL:
    case 4LL:
    case 6LL:
    case 7LL:
    case 8LL:
    case 9LL:
    case 12LL:
    case 13LL:
    case 14LL:
    case 17LL:
    case 18LL:
    case 19LL:
    case 20LL:
    case 23LL:
    case 24LL:
    case 25LL:
    case 26LL:
    case 27LL:
    case 29LL:
    case 30LL:
    case 33LL:
    case 34LL:
    case 35LL:
    case 36LL:
    case 37LL:
    case 38LL:
    case 40LL:
    case 41LL:
    case 42LL:
    case 43LL:
    case 45LL:
    case 46LL:
    case 47LL:
    case 48LL:
    case 50LL:
    case 51LL:
    case 52LL:
    case 53LL:
    case 54LL:
    case 55LL:
    case 56LL:
    case 57LL:
    case 58LL:
    case 60LL:
    case 61LL:
    case 62LL:
    case 63LL:
    case 64LL:
    case 65LL:
      return 6;
    case 5LL:
    case 16LL:
    case 22LL:
    case 67LL:
      return 4;
    case 10LL:
    case 15LL:
    case 21LL:
    case 31LL:
    case 66LL:
      return result;
    case 32LL:
    case 49LL:
      return 5;
    case 39LL:
    case 44LL:
      return 3;
    default:
      LOBYTE(v1) = v4;
      if ( v1 == 102421 || v1 == 102423 )
        return 3;
      return 6;
  }
}
