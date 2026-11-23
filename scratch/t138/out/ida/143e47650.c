bool sub_143E47650()
{
  __int64 *v0; // rax
  __int64 *v1; // rdx
  __int64 *v2; // rcx
  __int64 *v3; // rdi
  int v4; // r14d
  volatile signed __int32 *v5; // rsi
  __int64 v6; // rdi
  volatile signed __int32 *v7; // rcx
  __int64 v8; // rcx
  char v10[8]; // [rsp+28h] [rbp-28h] BYREF
  volatile signed __int32 *v11; // [rsp+30h] [rbp-20h] BYREF
  int v12; // [rsp+38h] [rbp-18h] BYREF
  _QWORD v13[6]; // [rsp+40h] [rbp-10h] BYREF

  v13[1] = -2;
  v0 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
  v1 = (__int64 *)v0[1];
  v2 = v0;
  if ( *((_BYTE *)v1 + 25) == 0 )
  {
    v2 = **(__int64 ***)(*(_QWORD *)(qword_141ABD878 + 24) + 8LL);
    do
    {
      v3 = v1 + 2;
      if ( v1[4] >= (unsigned __int64)qword_141B5EDF0 )
      {
        v2 = v1;
        v3 = v1;
      }
      v1 = (__int64 *)*v3;
    }
    while ( *(_BYTE *)(*v3 + 25) == 0 );
  }
  v4 = 0;
  if ( *((_BYTE *)v2 + 25) != 0 )
  {
LABEL_7:
    v5 = nullptr;
    goto LABEL_8;
  }
  v5 = nullptr;
  if ( qword_141B5EDF0 >= (unsigned __int64)v2[4] && v2 != v0 )
  {
    v5 = (volatile signed __int32 *)v2[5];
    if ( v5 != nullptr )
    {
      _InterlockedIncrement(v5 + 2);
      goto LABEL_8;
    }
    goto LABEL_7;
  }
LABEL_8:
  sub_14080D0E0(a1: v10, a2: 0x1418E2C24LL);
  v6 = sub_1412EC810(a1: 264, a2: 7);
  *(_QWORD *)v6 = 0x700000000LL;
  strcpy((char *)(v6 + 8), "summary");
  _InterlockedIncrement((volatile signed __int32 *)v6);
  v13[0] = 0;
  _InterlockedIncrement((volatile signed __int32 *)v6);
  v13[0] = v6 + 4;
  (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, _QWORD *, char *))(*(_QWORD *)v5 + 208LL))(
    a1: v5,
    a2: &v11,
    a3: v13,
    a4: v10);
  if ( v11 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, int *, __int64))(*(_QWORD *)v11 + 152LL))(
      a1: v11,
      a2: &v12,
      a3: 3);
    v4 = v12;
    v7 = v11;
    if ( v11 != nullptr && _InterlockedDecrement(v11 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v7)(a1: v7, a2: 1);
  }
  v8 = v13[0];
  if ( v13[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13[0] - 4LL)) == 0 )
    sub_1412EC9A0(a1: v8 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v6) == 0 )
    sub_1412EC9A0(a1: v6);
  if ( _InterlockedDecrement(v5 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v5)(a1: v5, a2: 1);
  return v4 == 0;
}
