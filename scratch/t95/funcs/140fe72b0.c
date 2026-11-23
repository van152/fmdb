__int64 *__fastcall sub_140FE72B0(int *a1, int a2, __int64 *a3)
{
  unsigned __int64 v6; // rbx
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rax
  unsigned __int64 v11; // rcx
  __int64 *result; // rax
  __int64 v13[3]; // [rsp+20h] [rbp-30h] BYREF
  __int64 v14; // [rsp+38h] [rbp-18h] BYREF
  unsigned __int64 v15; // [rsp+40h] [rbp-10h]
  __int64 v16; // [rsp+48h] [rbp-8h]

  v16 = -2;
  if ( *a1 < 0 )
  {
    result = &qword_141B5A4A0;
    if ( a3 != &qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      return (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                          qword_141B5A4A0,
                          &qword_141B5A4A0,
                          a3);
    }
  }
  else
  {
    sub_1407C9510(v13);
    v6 = ((unsigned __int64)(unsigned int)a1[1] << 32) | *a1;
    v8 = sub_14083D4F0(v7);
    v15 = v6;
    v14 = v8 + 72;
    sub_140833EB0(v13, a2, &v14);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v14);
    sub_14083DDA0(&v14, v13);
    v9 = *a3;
    if ( &v14 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v9 + 16LL))(v9, a3);
      v10 = v14;
      v11 = v15;
      a3[1] = v15;
      *a3 = v10;
      v9 = sub_14083D4F0(v11) + 8;
      v15 = 0;
      v14 = v9;
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v9 + 16LL))(v9, &v14);
    return (__int64 *)sub_140833970(v13);
  }
  return result;
}
