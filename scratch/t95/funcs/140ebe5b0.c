_QWORD *__fastcall sub_140EBE5B0(__int64 *a1, _QWORD *a2, __int64 a3)
{
  __int64 v6; // rbx
  _QWORD *v7; // rsi

  v6 = *a1;
  v7 = *(_QWORD **)(*a1 + 8 * a3);
  if ( v7 != nullptr )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v7 + 16LL))(*v7, v7);
    sub_1400039E0(v7);
  }
  sub_141758A00();
  a1[1] -= 8;
  *a2 = v6 + 8 * a3;
  return a2;
}
