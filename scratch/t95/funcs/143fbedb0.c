char __fastcall sub_143FBEDB0(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al

  result = 0;
  if ( a2 > 1346793580 )
  {
    if ( a2 <= 1347905890 )
    {
      if ( a2 <= 1347185004 )
      {
        if ( a2 != 1346793581 )
        {
          if ( a2 != 1347176803 )
            return result;
          goto LABEL_37;
        }
        goto LABEL_38;
      }
      if ( a2 == 1347185005 )
        goto LABEL_38;
      if ( a2 != 1347905347 )
      {
        if ( a2 != 1347905351 )
          return result;
        goto LABEL_38;
      }
      goto LABEL_37;
    }
    if ( a2 > 1348036418 )
    {
      if ( a2 != 1348036419 )
      {
        if ( a2 != 1348101959 )
        {
          if ( a2 != 1348101955 )
            return result;
          goto LABEL_37;
        }
        goto LABEL_38;
      }
      goto LABEL_37;
    }
    if ( a2 == 1347905891 )
      goto LABEL_37;
    if ( a2 == 1347905901 || a2 == 1348036417 )
      goto LABEL_38;
  }
  else
  {
    if ( a2 > 1346792546 )
    {
      if ( a2 > 1346792808 )
      {
        if ( a2 == 1346792809 )
        {
          *(_BYTE *)(a1 + 41) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          return 1;
        }
        if ( a2 != 1346792813 )
        {
          if ( a2 != 1346793571 )
            return result;
          goto LABEL_37;
        }
        goto LABEL_38;
      }
      if ( a2 != 1346792547 )
      {
        if ( a2 != 1346792557 )
        {
          if ( a2 != 1346792803 )
            return result;
          goto LABEL_37;
        }
LABEL_38:
        *(_DWORD *)(a1 + 20) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return 1;
      }
LABEL_37:
      *(_DWORD *)(a1 + 24) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      return 1;
    }
    if ( a2 > 1346791277 )
    {
      if ( a2 == 1346791278 )
        goto LABEL_38;
      if ( a2 != 1346791779 )
      {
        if ( a2 != 1346791789 )
          return result;
        goto LABEL_38;
      }
      goto LABEL_37;
    }
    if ( a2 == 1346789986 || a2 == 1346791267 )
      goto LABEL_37;
  }
  return result;
}
