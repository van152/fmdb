// THUNK ALIAS -> sub_1442B52E0 (jmp:0x1413ca830->0x1442b52e0)
_DWORD *__fastcall sub_1442B52E0(_DWORD *a1, __int64 *a2)
{
  __int64 v3; // rcx
  int v4; // edx
  signed int v5; // esi
  int v6; // edi
  __int16 v7; // ax
  int v8; // r9d
  int v9; // r8d
  int v11; // [rsp+38h] [rbp-40h] BYREF
  __int16 v12[2]; // [rsp+40h] [rbp-38h] BYREF
  unsigned __int8 v13; // [rsp+44h] [rbp-34h]
  unsigned __int16 v14; // [rsp+48h] [rbp-30h]

  v3 = *a2;
  if ( *a2 != 0 )
  {
    v4 = (__int64)(v3 + ((v3 >> 63) & 0xFFFFFFFFFAD9A401uLL)) / 86400000;
    v5 = (int)(-86400000 * v4 + v3 + (((-86400000 * v4 + (int)v3) >> 31) & 0xFAD9A401)) % 86400000
       - (((-86400000 * v4 + (int)v3) >> 31) & 0xFAD9A401);
    v6 = (int)(v5 + ((v5 >> 31) & 0xFFC91181)) / 3600000;
    v11 = v4;
    sub_14082C700(&v11, v12);
    v7 = v12[0];
    v8 = v13;
    v9 = v14;
    *a1 = 0;
    sub_140051D30(
      (_DWORD)a1,
      100 * (char)v6
    + (char)(((((unsigned __int64)(1172812403LL * (int)(v5 - 3600000 * v6 + (((v5 - 3600000 * v6) >> 31) & 0xFFFF15A1))) >> 32)
             & 0x80000000) != 0LL)
           + (int)(v5 - 3600000 * v6 + (((v5 - 3600000 * v6) >> 31) & 0xFFFF15A1)) / 0xEA60uLL),
      v9,
      v8,
      v7,
      0);
  }
  else
  {
    *a1 = 124518401;
  }
  return a1;
}
