char __fastcall sub_144531C80(__int64 a1, int a2, __int64 **a3)
{
  unsigned int v4; // eax
  double *v5; // rax

  if ( a2 != 1130723442 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  *(float *)(a1 + 56) = (*(float (__fastcall **)(__int64 *, __int64 **))(**a3 + 96))(*a3, a3);
  v4 = sub_14157FD30(*(unsigned int *)(a1 + 12));
  if ( (_BYTE)v4 != 0xFF )
  {
    v5 = (double *)sub_140D9E1C0(v4);
    if ( v5 != nullptr )
      *v5 = *(float *)(a1 + 56);
  }
  return 1;
}
