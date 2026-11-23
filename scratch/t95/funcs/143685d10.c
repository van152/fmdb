__int64 *__fastcall sub_143685D10(__int64 a1, __int64 *a2, unsigned int a3)
{
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rcx
  __int64 v10; // [rsp+20h] [rbp-10h] BYREF
  __int64 v11; // [rsp+28h] [rbp-8h]
  __int64 v12; // [rsp+30h] [rbp+0h]

  v12 = -2;
  v11 = 0;
  v10 = sub_14083D4F0(a1) + 8;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD, __int64 *))(*(_QWORD *)a1 + 16LL))(a1, a3, &v10) != 0 )
  {
    v6 = v10;
    v7 = v11;
    a2[1] = v11;
    *a2 = v6;
    v8 = sub_14083D4F0(v7) + 8;
    v11 = 0;
    v10 = v8;
  }
  else
  {
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      a2);
    v8 = v10;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v10);
  return a2;
}
