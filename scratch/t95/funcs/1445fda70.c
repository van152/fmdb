__int64 __fastcall sub_1445FDA70(_QWORD *a1, __int64 *a2)
{
  __int64 v2; // rbx
  __int64 v3; // rdx
  __int64 result; // rax
  __int64 v6; // rcx
  __int64 *v7; // rax
  __int64 *v8; // rdx
  __int64 v9; // rdi
  _QWORD v10[2]; // [rsp+28h] [rbp-30h] BYREF
  int v11[8]; // [rsp+38h] [rbp-20h] BYREF

  v2 = *a2;
  v3 = a2[1];
  if ( v2 == v3 )
    return 0;
  result = 0;
  v6 = v2;
  while ( *(_DWORD *)v6 != 1986096245 )
  {
    v6 += 16;
    if ( v6 == v3 )
      return result;
  }
  if ( v6 == v3 || *(_QWORD *)(v6 + 8) == 0 )
    return 0;
  v10[1] = 0x76C0001076C0001LL;
  v7 = nullptr;
  while ( *(_DWORD *)v2 != 1986096245 )
  {
    v2 += 16;
    if ( v2 == v3 )
      goto LABEL_16;
  }
  if ( v2 == v3 )
    v7 = nullptr;
  else
    v7 = *(__int64 **)(v2 + 8);
LABEL_16:
  v8 = &qword_141B5A4A0;
  if ( v7 != nullptr )
    v8 = v7;
  v9 = qword_141B5FE60;
  sub_140FE7960((__int64)v11, v8, 0x6167726Du);
  v10[0] = sub_140FA3700(v9, v11);
  return sub_14104DD70(*a1, v10);
}
