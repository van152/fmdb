__int64 __fastcall sub_1411DCA60(_QWORD *a1, unsigned __int64 a2)
{
  __int64 v3; // rax
  unsigned __int64 v4; // rbx
  __int64 v5; // rax
  __int64 result; // rax
  char v8; // al
  __int64 v9; // r9
  __int64 v10; // rdi
  __int64 v11; // rdi
  unsigned __int64 v12; // rsi
  unsigned __int64 v13; // rdi
  __int64 v14; // rdx
  __int64 i; // rdi
  __int64 v16; // rcx

  v3 = a1[3];
  v4 = (a1[4] - v3) >> 3;
  if ( v4 > a2 )
  {
    v5 = v3 + 8 * a2;
    return *(_QWORD *)v5;
  }
  v8 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(qword_141B5AD60);
  v9 = a1[6];
  v10 = a1[7];
  if ( v8 != 0 )
  {
    v11 = v10 - v9;
    if ( v11 != 0 )
    {
      v12 = a2 - v4;
      v13 = v11 >> 3;
      v14 = 1;
      if ( v13 >= 2 )
        v14 = v13;
      for ( i = 0; v14 != i; ++i )
      {
        result = *(_QWORD *)(v9 + 8 * i);
        v16 = 368;
        if ( *(_BYTE *)(result + 47) == 0 )
          v16 = 216;
        if ( *(_QWORD *)(*(_QWORD *)(result + 48) + v16) != 0 )
        {
          if ( v12 == 0 )
            return result;
          --v12;
        }
      }
    }
  }
  else if ( v4 + ((v10 - v9) >> 3) > a2 )
  {
    v5 = v9 + 8 * (a2 - v4);
    return *(_QWORD *)v5;
  }
  return 0;
}
