__int64 __fastcall sub_14155E670(__int64 a1, int a2)
{
  __int64 result; // rax

  result = 0;
  if ( a2 <= 1349348911 )
  {
    switch ( a2 )
    {
      case 1348564016:
        goto LABEL_14;
      case 1348564017:
LABEL_9:
        a1 += 5;
        goto LABEL_14;
      case 1348564018:
LABEL_10:
        a1 += 10;
        goto LABEL_14;
      case 1348564019:
LABEL_11:
        a1 += 15;
        goto LABEL_14;
      case 1348564020:
LABEL_12:
        a1 += 20;
        goto LABEL_14;
      case 1348564021:
LABEL_13:
        a1 += 25;
LABEL_14:
        result = a1;
        break;
      default:
        switch ( a2 )
        {
          case 1348890928:
            goto LABEL_14;
          case 1348890929:
            goto LABEL_9;
          case 1348890930:
            goto LABEL_10;
          case 1348890931:
            goto LABEL_11;
          case 1348890932:
            goto LABEL_12;
          case 1348890933:
            goto LABEL_13;
          default:
            return result;
        }
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1349348912:
        goto LABEL_14;
      case 1349348913:
        goto LABEL_9;
      case 1349348914:
        goto LABEL_10;
      case 1349348915:
        goto LABEL_11;
      case 1349348916:
        goto LABEL_12;
      case 1349348917:
        goto LABEL_13;
      default:
        switch ( a2 )
        {
          case 1349351472:
            goto LABEL_14;
          case 1349351473:
            goto LABEL_9;
          case 1349351474:
            goto LABEL_10;
          case 1349351475:
            goto LABEL_11;
          case 1349351476:
            goto LABEL_12;
          case 1349351477:
            goto LABEL_13;
          default:
            switch ( a2 )
            {
              case 1349476912:
                goto LABEL_14;
              case 1349476913:
                goto LABEL_9;
              case 1349476914:
                goto LABEL_10;
              case 1349476915:
                goto LABEL_11;
              case 1349476916:
                goto LABEL_12;
              case 1349476917:
                goto LABEL_13;
              default:
                return result;
            }
        }
    }
  }
  return result;
}
