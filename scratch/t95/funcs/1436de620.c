__int64 *__fastcall sub_1436DE620(__int64 *a1, _DWORD *a2)
{
  unsigned int v3; // ecx
  unsigned int v4; // eax
  int v5; // eax
  unsigned int v6; // ebx
  __int64 v7; // rdi
  volatile signed __int32 *v8; // rcx
  __int64 v9; // rax
  __int64 *v10; // rax
  _BYTE v12[56]; // [rsp+20h] [rbp-38h] BYREF

  v3 = *a2 + 99;
  v4 = *a2 - 1950;
  if ( v3 >= 0xC7 && v4 > 0x64 )
  {
    sub_14080E2E0(v12, 31, 0x14191E641LL);
    *a1 = 0;
    v5 = sub_141758DB0(v12);
    v6 = v5;
    if ( v5 <= 0 )
    {
      v9 = 0;
    }
    else
    {
      v7 = sub_1412EC810(264, (unsigned int)v5);
      *(_DWORD *)v7 = 0;
      *(_DWORD *)(v7 + 4) = v6;
      sub_141758A00();
      *(_BYTE *)(v7 + v6 + 8) = 0;
      if ( *a1 != 0 )
      {
        v8 = (volatile signed __int32 *)(*a1 - 4);
        if ( _InterlockedDecrement(v8) == 0 )
          sub_1412EC9A0((__int64)v8);
      }
      v9 = v7 + 4;
      *a1 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v7);
    }
LABEL_17:
    *a1 = v9;
    return a1;
  }
  if ( qword_141B59ED8 != 0 )
  {
    if ( v3 <= 0xC6 )
    {
      v10 = (__int64 *)(qword_141B59ED8 + 8LL * v3 + 8);
      goto LABEL_14;
    }
    if ( v4 <= 0x64 )
    {
      v10 = (__int64 *)(qword_141B59ED8 + 8LL * v4 + 1600);
LABEL_14:
      *a1 = 0;
      if ( v10 != a1 )
      {
        v9 = *v10;
        if ( v9 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v9 - 4));
        goto LABEL_17;
      }
      return a1;
    }
  }
  sub_14080B990(a1, 0x14191E641LL, (unsigned int)*a2);
  return a1;
}
