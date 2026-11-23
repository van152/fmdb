__int64 __fastcall sub_143BA70F0(__int64 a1, int a2)
{
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rax
  int v6; // eax

  if ( a2 != 0 )
  {
    *(_QWORD *)(a1 + 680) = 0x141876F88LL;
    *(_QWORD *)(a1 + 8) = 0x1418795DCLL;
    *(_QWORD *)(a1 + 640) = -1;
    *(_DWORD *)(a1 + 648) = 0;
    *(_QWORD *)(a1 + 632) = 0x141889DA8LL;
    *(_QWORD *)(a1 + 656) = 0;
    sub_140DD7950(a1: a1 + 672, a2: 0);
  }
  *(_QWORD *)a1 = 0x14187A428LL;
  *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 4LL) + a1 + 8) = 0x14187A8F8LL;
  v3 = *(int *)(*(_QWORD *)(a1 + 8) + 4LL);
  *(_DWORD *)(v3 + a1 + 4) = v3 - 16;
  *(_QWORD *)a1 = 0x1418795F8LL;
  *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 8) = 0x141879AC8LL;
  *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 4LL) + a1 + 8) = 0x141879B18LL;
  v4 = *(int *)(*(_QWORD *)(a1 + 8) + 4LL);
  *(_DWORD *)(v4 + a1 + 4) = v4 - 624;
  v5 = *(int *)(*(_QWORD *)(a1 + 8) + 8LL);
  *(_DWORD *)(v5 + a1 + 4) = v5 - 664;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(a1: &unk_141B59A68);
        sub_141751048(a1: sub_1407E4B20);
        sub_141750EA0(a1: &dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  sub_141758A10(a1: a1 + 16, a2: 0, a3: 175);
  *(_DWORD *)(a1 + 192) = -1;
  *(_WORD *)(a1 + 196) = 1900;
  sub_141758A10(a1: a1 + 200, a2: 0, a3: 136);
  v6 = dword_141AAE084;
  *(_DWORD *)(a1 + 336) = dword_141AAE084;
  *(_DWORD *)(a1 + 340) = v6;
  *(_DWORD *)(a1 + 344) = -1;
  *(_QWORD *)(a1 + 348) = 0xC000FFFFC000FFFFuLL;
  *(_QWORD *)(a1 + 356) = 0xFFFFC000FFFFLL;
  *(_BYTE *)(a1 + 366) = 90;
  *(_WORD *)(a1 + 364) = 0;
  *(_QWORD *)(a1 + 404) = 0;
  *(_QWORD *)(a1 + 399) = 0;
  *(_QWORD *)(a1 + 391) = 0;
  *(_QWORD *)(a1 + 383) = 0;
  *(_QWORD *)(a1 + 375) = 0;
  *(_QWORD *)(a1 + 367) = 0;
  *(_QWORD *)(a1 + 412) = 0x76C0001076C0001LL;
  *(_DWORD *)(a1 + 420) = 124518401;
  *(_WORD *)(a1 + 448) = 0;
  *(_QWORD *)(a1 + 440) = 0;
  *(_QWORD *)(a1 + 432) = 0;
  *(_QWORD *)(a1 + 424) = 0;
  *(_BYTE *)(a1 + 450) = -1;
  *(_DWORD *)(a1 + 458) = 0;
  *(_QWORD *)(a1 + 451) = 0;
  *(_QWORD *)(a1 + 464) = -1;
  *(_QWORD *)(a1 + 472) = 0xFFFFFFFF00000000uLL;
  *(_QWORD *)(a1 + 480) = -1;
  *(_DWORD *)(a1 + 488) = 0;
  *(_QWORD *)(a1 + 492) = 0x76C0001076C0001LL;
  *(_DWORD *)(a1 + 500) = -16374000;
  *(_WORD *)(a1 + 504) = 10000;
  *(_QWORD *)(a1 + 512) = 0;
  *(_QWORD *)(a1 + 506) = 0;
  sub_14085C1E0(a1: a1 + 520);
  *(_QWORD *)(a1 + 589) = 0;
  *(_QWORD *)(a1 + 596) = 0;
  *(_BYTE *)(a1 + 604) = -1;
  *(_DWORD *)(a1 + 605) = 0;
  *(_WORD *)(a1 + 609) = -1;
  *(_DWORD *)(a1 + 611) = 0;
  *(_BYTE *)(a1 + 615) = -1;
  *(_DWORD *)(a1 + 616) = 0;
  return a1;
}
