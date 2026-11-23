int *__fastcall sub_143E34390(_DWORD *a1, int *a2)
{
  _DWORD *v3; // rdi
  int v4; // esi
  unsigned int v5; // eax
  int v6; // esi
  bool v7; // zf
  int v8; // eax
  _QWORD v10[8]; // [rsp+20h] [rbp-10h] BYREF

  v10[2] = -2;
  v3 = a1;
  v10[1] = 0;
  v10[0] = sub_14083D4F0(a1) + 8;
  v4 = v3[2];
  LODWORD(v3) = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v3 + 56LL))(v3);
  (*(void (__fastcall **)(_QWORD, _QWORD *, int *))(*(_QWORD *)v10[0] + 24LL))(v10[0], v10, a2 + 2);
  v5 = v4 & (unsigned int)v3;
  v6 = ((_DWORD)v3 << 24) | v4 & 0x7FFFFF;
  v7 = v5 == -1;
  v8 = -8388609;
  if ( !v7 )
    v8 = v6;
  *a2 = v8;
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v10[0] + 16LL))(v10[0], v10);
  return a2;
}
