__int64 __fastcall sub_143A27780(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  __int64 v9; // rax
  unsigned __int64 v10; // rsi
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  __int64 v13; // [rsp+30h] [rbp-30h] BYREF
  char v14[8]; // [rsp+38h] [rbp-28h] BYREF
  __int64 v15; // [rsp+40h] [rbp-20h] BYREF
  __int64 v16; // [rsp+48h] [rbp-18h] BYREF
  _QWORD v17[6]; // [rsp+50h] [rbp-10h] BYREF

  v17[1] = -2;
  sub_14080D0E0(a1: v14, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 10);
  *(_QWORD *)v4 = 0xA00000000LL;
  strcpy((char *)(v4 + 8), "friend_man");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v15 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v15 = v4 + 4;
  v13 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v16,
          a3: &v15,
          a4: v14),
        v16 != 0) )
  {
    LOWORD(v5) = 32;
    sub_1407D1280(a1: (unsigned int)&v13, a2: (unsigned int)v17, a3: (unsigned int)&v16, a4: v5, a5: 0);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v16;
    if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  else
  {
    v17[0] = 0;
  }
  v7 = v15;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  if ( v17[0] != 0 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD *, _QWORD *))(*a1 + 160LL))(a1, a2: v17) != 0 )
    {
      v8 = (void (__fastcall ***)(_QWORD, __int64))v17[0];
      if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] + 8LL)) == 0 )
        (**v8)(a1: v8, a2: 1);
      v17[0] = 0;
      v9 = a1[5];
      if ( a1[6] == v9 )
      {
        LOBYTE(v4) = 1;
      }
      else
      {
        v10 = 0;
        do
        {
          LODWORD(v4) = sub_14096EA70(a1: *(_QWORD *)(v9 + 8 * v10), a2);
          if ( (_BYTE)v4 == 0 )
            break;
          ++v10;
          v9 = a1[5];
        }
        while ( v10 < (a1[6] - v9) >> 3 );
      }
    }
    else
    {
      LODWORD(v4) = 0;
    }
    v11 = (void (__fastcall ***)(_QWORD, __int64))v17[0];
    if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] + 8LL)) == 0 )
      (**v11)(a1: v11, a2: 1);
  }
  else
  {
    LODWORD(v4) = 0;
  }
  return (unsigned int)v4;
}
