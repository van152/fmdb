__int64 __fastcall sub_1443B6D30(__int64 a1)
{
  __int64 v1; // rax
  __int64 *v2; // rcx
  __int64 v3; // r8
  __int64 v4; // rdx
  __int64 v5; // rcx
  __int64 v6; // rcx
  __int64 *v7; // rax
  __int64 v8; // rax
  bool v9; // zf
  unsigned __int8 v10; // al
  unsigned int v11; // ecx
  bool v12; // cc
  __int64 result; // rax
  unsigned __int16 v14; // ax
  __int16 v15; // r9
  __int16 v16; // ax
  unsigned int v17; // edx
  char v18; // al
  __int64 v19; // r9
  int v20; // edx
  char v21; // dl
  char v22; // cl
  int v23; // r8d
  char v24; // al
  char v25; // cl

  v1 = *(_QWORD *)(a1 + 8);
  if ( v1 == 0 )
    return 9;
  v2 = *(__int64 **)(v1 + 24);
  if ( v2 == *(__int64 **)(v1 + 32) )
  {
LABEL_8:
    v10 = 0;
  }
  else
  {
    v3 = *v2;
    v4 = *v2;
    while ( 1 )
    {
      v5 = *(_QWORD *)(v4 + 120);
      if ( v5 != 0 )
        break;
      v6 = *(_QWORD *)(v4 + 48);
      if ( v6 != 0 )
      {
        v7 = *(__int64 **)(v6 + 24);
        if ( *(__int64 **)(v6 + 32) != v7 )
        {
          v8 = *v7;
          v9 = v8 == v4;
          v4 = v8;
          if ( !v9 )
            continue;
        }
      }
      goto LABEL_8;
    }
    v14 = *(_WORD *)(v5 + 42);
    v15 = HIWORD(dword_141AAE084) - v14;
    v9 = (*(_WORD *)(v5 + 40) & 0x1FF ^ 1 | v14 ^ 0x76C) == 0;
    v16 = 30;
    if ( !v9 )
      v16 = v15;
    v17 = 2 * (((unsigned int)(10923 * v16) >> 31) + ((unsigned int)(10923 * v16) >> 17));
    if ( (__int16)(2 * (v16 / 12)) >= 20 )
      LOBYTE(v17) = 20;
    v18 = 5 * (v16 < 11) + 9 - v17;
    v19 = *(int *)(v5 + 108);
    v20 = 2 * ((int)v19 / 10000);
    if ( (__int16)(2 * ((int)v19 / 10000)) >= 20 )
      LOBYTE(v20) = 20;
    v21 = v18 + v20;
    v22 = v21 - 3;
    if ( v19 >= 5000 )
      v22 = v21;
    if ( v3 == 0 )
      goto LABEL_25;
    v23 = *(__int16 *)(v3 + 168);
    v24 = 6;
    if ( v22 >= 5 )
      v24 = v22;
    if ( v23 > 2499 )
      v25 = v24;
    else
LABEL_25:
      v25 = v22 - 2;
    v10 = 1;
    if ( v25 >= 2 )
      v10 = v25;
  }
  v11 = v10;
  v12 = (char)v10 < 20;
  result = 20;
  if ( v12 )
    return v11;
  return result;
}
